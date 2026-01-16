from fastapi import FastAPI

from app.core.settings import settings
from app.routers import mainRouter

def createApp() -> FastAPI:
    try:
        app = FastAPI(
            title=settings.appName,
            version=settings.appVersion
        )

        app.include_router(mainRouter)
        
        return app
    except Exception as e:
        raise e

app = createApp()
