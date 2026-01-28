"""
Lifespan 데코레이터
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시
    logger.writeLog("info", "애플리케이션 시작")
    yield
    # 종료 시
    logger.writeLog("info", "애플리케이션 종료 중...")
    logger.shutdown()
