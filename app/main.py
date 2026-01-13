from fastapi import FastAPI

from app.core.settings import settings
from app.core.routerLoader import loadRouters

def createApp() -> FastAPI:
    try:
        app = FastAPI(
            title=settings.appName,
            version=settings.appVersion
        )

        loadRouters(app)
        
        return app
    except Exception as e:
        raise e

app = createApp()
