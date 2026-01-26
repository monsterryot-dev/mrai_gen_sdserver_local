"""
google imagen을 이용한 이미지 생성 라우터 모듈
"""
from fastapi import APIRouter, Depends

from app.core.decorators.exception import endpointContext
from app.services.google.imagen import GoogleImagenService

from app.schemas.requests.google.imagen import ImagenRequestPost

imagenRouter = APIRouter()

@imagenRouter.post("/generate/txt")
@endpointContext
async def generateImageFromText(
    request: ImagenRequestPost = Depends(ImagenRequestPost.asForm)
):
    service = GoogleImagenService()
    result = service.makeImage(request)
    return result
