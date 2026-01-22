"""
Uvicorn을 사용하여 FastAPI 서버 시작
개발자 모드에서 사용하세요
"""
import uvicorn

from app.utils.serverConfig import getServerInfo

if __name__ == "__main__":
    print("서버 시작 중...")
    try:
        serverInfo = getServerInfo()

        uvicorn.run(
            serverInfo["app"],
            host=serverInfo["host"],
            port=serverInfo["port"],
            reload=serverInfo["reload"],
        )
    except KeyboardInterrupt:
        print("서버 중지 요청 받음.")
    except Exception as e:
        print(f"서버 오류: {e}")
    finally:
        print("서버 중지.")