from fastapi import FastAPI

from app.core.settings import settings

def createApp() -> FastAPI:
    try:
        app = FastAPI(
            title=settings.appName,
            version=settings.appVersion
        )
        
        return app
    except Exception as e:
        raise e

app = createApp()
