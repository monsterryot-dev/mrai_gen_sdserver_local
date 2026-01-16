"""
google imagen을 이용한 이미지 생성 라우터 모듈
"""
from fastapi import APIRouter

imagenRouter = APIRouter()

@imagenRouter.post("/generate/txt")
async def generateImageFromText():
    return {"message": "텍스트로부터 이미지 생성 엔드포인트"}

@imagenRouter.post("/generate/img")
async def generateImageFromImage():
    return {"message": "이미지로부터 이미지 생성 엔드포인트"}
