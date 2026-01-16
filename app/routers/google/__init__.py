from fastapi import APIRouter

googleRouter = APIRouter()

# 하위 라우터 등록
from app.routers.google.imagen import imagenRouter
from app.routers.google.nanoBanana import nanoBananaRouter

googleRouter.include_router(
    imagenRouter, 
    prefix="/imagen", 
    tags=["imagen"]
)
googleRouter.include_router(
    nanoBananaRouter, 
    prefix="/nanoBanana", 
    tags=["nanoBanana"]
)