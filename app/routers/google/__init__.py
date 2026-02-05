from fastapi import APIRouter

googleRouter = APIRouter()

# 하위 라우터 등록
from app.routers.google.imagen import imagenRouter
from app.routers.google.gemini import geminiRouter

googleRouter.include_router(
    imagenRouter, 
    prefix="/imagen", 
    tags=["imagen"]
)
googleRouter.include_router(
    geminiRouter,
    prefix="/gemini",
    tags=["gemini"]
)