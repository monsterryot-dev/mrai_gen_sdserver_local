"""
FastAPI 라우터 설정
"""
from fastapi import FastAPI

from app.routers import mainRouter
from app.core.handler import settingHandlers
from app.core.decorators.exception import routerLoadContext

def settingRouter(app:FastAPI) -> FastAPI:
    with routerLoadContext('메인'):
        app = loadHandlers(app)

        app = loadRouters(app)

        return app
    
def loadRouters(app:FastAPI) -> FastAPI:
    with routerLoadContext('api'):
        app.include_router(mainRouter)

        return app
    
def loadHandlers(app:FastAPI) -> FastAPI:
    with routerLoadContext('핸들러'):
        app = settingHandlers(app)

        return app