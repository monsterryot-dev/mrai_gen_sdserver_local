import os
import sys
import uvicorn
import threading
import win32event
import win32service
import servicemanager
import win32serviceutil

# cx_Freeze 환경에서 동작하도록 경로 추가
if getattr(sys, 'frozen', False):
    currentDir = os.path.dirname(sys.executable)
else:
    currentDir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, currentDir)

# 작업 디렉토리 명시적 설정
os.chdir(currentDir)

from app.main import app
from app.utils.serverConfig import getServerInfo

class MraiSdService(win32serviceutil.ServiceFramework):
    _svc_name_ = "mrai sd service"
    _svc_display_name_ = "MRAI SD 서비스"
    _svc_description_ = "MRAI SD 서비스입니다."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True
        self.server = None
        self.server_thread = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.hWaitStop)
    
        # 서버 종료
        if self.server:
            self.server.should_exit = True

    def runServer(self):
        """
        uvicorn 스레트 실행
        """
        try:
            serverInfo = getServerInfo()
            config = uvicorn.Config(
                app=app,
                host=serverInfo["host"],
                port=serverInfo["port"],
                log_level="info",
                access_log=True,
                use_colors=True,
            )
            self.server = uvicorn.Server(config)
            self.server.run()
        except Exception as e:
            servicemanager.LogErrorMsg(f"서버 실행 중 오류 발생: {e}")

    def main(self):
        try:
            self.serverThread = threading.Thread(
                target=self.runServer, 
                daemon=True
            )
            self.serverThread.start()

            while self.running:
                rc = win32event.WaitForSingleObject(
                    self.hWaitStop, 
                    5000
                )
                if rc == win32event.WAIT_OBJECT_0:
                    break
            
            if self.server:
                self.server.should_exit = True
            
            if self.serverThread and self.serverThread.is_alive():
                self.serverThread.join(timeout=10)
        except Exception as e:
            servicemanager.LogErrorMsg(f"서비스 메인 오류: {str(e)}")
        finally:
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        win32serviceutil.HandleCommandLine(MraiSdService)
    else:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MraiSdService)
        servicemanager.StartServiceCtrlDispatcher()