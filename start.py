import uvicorn

from app.utils.serverConfig import getServerInfo

if __name__ == "__main__":
    try:
        serverInfo = getServerInfo()
        
        uvicorn.run(
            "app.main:app",
            host=serverInfo["host"],
            port=serverInfo["port"],
            reload=serverInfo["reload"],
        )
                
    except Exception as e:
        print(f"Error starting server: \n {e}")