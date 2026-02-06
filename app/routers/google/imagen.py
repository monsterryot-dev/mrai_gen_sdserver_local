"""
google imagen 관련 라우터 모듈
"""
from fastapi import APIRouter, Depends

from app.core.decorators.exception import endpointContext

from app.services.google.imagen import googleImagenTestService, googleImagenService

from app.schemas.requests.google.imagen import ImagenRequestPost

imagenRouter = APIRouter()

@imagenRouter.post("/")
@endpointContext
async def generateGoogleImagen(request: ImagenRequestPost = Depends(ImagenRequestPost.asForm)):
    if request.test == True:
        return  googleImagenTestService()
            
    result = googleImagenService(request)
    return result