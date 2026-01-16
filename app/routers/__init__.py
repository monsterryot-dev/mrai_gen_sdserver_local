"""
V1 라우터 메인 모듈
"""
from fastapi import APIRouter

mainRouter = APIRouter(
    prefix="/api",
    tags=["api"],
)

# 하위 라우터 등록
from app.routers.google import googleRouter
from app.routers.sdxl import sdxlRouter

mainRouter.include_router(
    googleRouter, 
    prefix="/google", 
    tags=["google"]
)
mainRouter.include_router(
    sdxlRouter, 
    prefix="/sdxl", 
    tags=["sdxl"]
)