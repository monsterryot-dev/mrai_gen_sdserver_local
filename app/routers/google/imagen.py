"""
google imagen을 이용한 이미지 생성 라우터 모듈
"""
from fastapi import APIRouter, Depends

from app.schemas.google.imagen import ImagenRequestPost

imagenRouter = APIRouter()

@imagenRouter.post("/generate/txt")
async def generateImageFromText(
    request: ImagenRequestPost = Depends(ImagenRequestPost.asForm)
):
    try:
        print(f"Requested data: {request}")
        return {"message": "텍스트로부터 이미지 생성 엔드포인트"}
    except Exception as e:
        return {"error": str(e)}

# @imagenRouter.post("/generate/img")
# async def generateImageFromImage():
#     return {"message": "이미지로부터 이미지 생성 엔드포인트"}
