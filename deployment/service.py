"""
Windows 서비스로 MRAI SD 서버 실행
"""
import os
import sys
import uvicorn
import threading
import win32event
import win32service
import servicemanager
import win32serviceutil

# 상수 설정
ScvName = "mrai sd service"
ScvDisplayName = "MRAI SD 서비스"
ScvDescription = "MRAI SD 서비스입니다."

# cx_Freeze 환경에서 동작하도록 경로 추가
if getattr(sys, 'frozen', False):
    rootDir = os.path.dirname(sys.executable)
else:
    rootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, rootDir)

# 작업 디렉토리를 루트로 설정
os.chdir(rootDir)
 
from app.main import app
from app.utils.serverConfig import getServerInfo

class MraiSdService(win32serviceutil.ServiceFramework):
    _svc_name_ = ScvName
    _svc_display_name_ = ScvDisplayName
    _svc_description_ = ScvDescription
    isRunning = False
    server = None
    serverThread = None

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

        # 초기 상태 설정
        self.server = None
        self.serverThread = None

        print("MRAI SD 서비스 초기화 완료.")

    def svcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.isRunning = False
        win32event.SetEvent(self.hWaitStop)

        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STOPPED,
            (self._svc_name_, '')
        )

        # 서버 종료
        if self.server:
            self.server.shouldExit = True 
        

    def svcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)

        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self._main()

    def _main(self):
        try:
            self.serverThread = threading.Thread(
                target=self._runServer(),
                daemon=True
            )
            self.serverThread.start()

            while self.isRunning:
                rc = win32event.WaitForSingleObject(
                    self.hWaitStop,
                    5000
                )
                if rc == win32event.WAIT_OBJECT_0:
                    break
                if self.server:
                    self.server.shouldExit = True
                if self.serverThread and self.serverThread.is_alive():
                    self.serverThread.join(timeout=10)
        except Exception as e:
            servicemanager.LogErrorMsg(f"서비스 메인 오류: {str(e)}")
        finally:
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def _runServer(self):
        try:
            serverInfo = getServerInfo()
            config = uvicorn.Config(
                app=app,
                host=serverInfo['host'],
                port=serverInfo['port'],
                log_level="info",
                access_log=False,
                use_colors=False
            )
            self.server = uvicorn.Server(config)
            self.server.run()
        except Exception as e:
            servicemanager.LogErrorMsg(f"서버 오류: {str(e)}")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        win32serviceutil.HandleCommandLine(MraiSdService)
    else:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MraiSdService)
        servicemanager.StartServiceCtrlDispatcher()