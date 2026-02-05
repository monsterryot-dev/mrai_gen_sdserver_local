"""
Lifespan 데코레이터
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.logger import logger

from app.constants.messages import appMessage

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시
    logger.writeLog("info", appMessage["startup"])
    yield
    # 종료 시
    logger.writeLog("info", appMessage["shutdown"])
    logger.shutdown()
