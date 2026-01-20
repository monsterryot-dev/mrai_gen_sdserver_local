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