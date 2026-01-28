"""
FastAPI 애플리케이션 생성 및 설정
"""
from fastapi import FastAPI

from app.core.logger import logger
from app.core.settings import settings
from app.core.settingRouter import settingRouter
from app.core.decorators.lifespan import lifespan

def createApp() -> FastAPI:
    try:
        app = FastAPI(
            title=settings.appName,
            version=settings.appVersion,
            lifespan=lifespan
        )

        app = settingRouter(app)
        
        return app
    except Exception as e:
        logger.writeLog("error", f"애플리케이션 생성 오류: {e}")

app = createApp()
