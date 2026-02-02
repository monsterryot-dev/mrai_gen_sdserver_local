"""
google 이미지 생성 라우터 모듈
"""
from fastapi import APIRouter, Depends

from app.core.decorators.exception import endpointContext
from app.services.google.txt2img import GoogleTxt2ImgService

from app.schemas.requests.google.txt2img import TextToImageRequestPost

generateRouter = APIRouter()

@generateRouter.post("/txt")
@endpointContext
async def generateTextToImage(
    request: TextToImageRequestPost = Depends(TextToImageRequestPost.asForm)
):
    service = GoogleTxt2ImgService()
    result = service.makeImage(request)
    return result

@generateRouter.post("img")
@endpointContext
async def generateImageToImage():
    pass