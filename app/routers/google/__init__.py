from fastapi import APIRouter

googleRouter = APIRouter()

# 하위 라우터 등록
from app.routers.google.generate import generateRouter

googleRouter.include_router(
    generateRouter, 
    prefix="/generate", 
    tags=["generate"]
)