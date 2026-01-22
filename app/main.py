"""
FastAPI 애플리케이션 생성 및 설정
"""
from fastapi import FastAPI

from app.core.settings import settings
from app.core.settingRouter import settingRouter

def createApp() -> FastAPI:
    try:
        app = FastAPI(
            title=settings.appName,
            version=settings.appVersion
        )

        app = settingRouter(app)
        
        return app
    except Exception as e:
        raise e

app = createApp()
