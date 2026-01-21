# INFO: UVICORN DEBUG RUNNER [개발자 모드시 해당 파일을 실행하여 서버를 구동합니다.]
import uvicorn

from app.utils.serverConfig import getServerInfo
from app.core.decorators.exception import serverStartContext

if __name__ == "__main__":
    with serverStartContext():
        serverInfo = getServerInfo()

        uvicorn.run(
            serverInfo["app"],
            host=serverInfo["host"],
            port=serverInfo["port"],
            reload=serverInfo["reload"],
        )