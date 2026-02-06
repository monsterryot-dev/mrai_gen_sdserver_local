"""
google gemini 관련 라우터 모듈
"""
from fastapi import APIRouter, Depends

from app.core.decorators.exception import endpointContext

from app.services.google.gemini.generate import googleGeminiTestService, googleGeminiTxt2ImgService

from app.schemas.requests.google.gemini.generate import (
    GeminiGenerateRequestPost
)

geminiRouter = APIRouter()

@geminiRouter.post("/")
@endpointContext
async def generateGoogleGemini(
    request: GeminiGenerateRequestPost = Depends(GeminiGenerateRequestPost.asForm),
):
    if request.test == True:
        return  googleGeminiTestService()
    
    if request.genType == "txt2img":
        return googleGeminiTxt2ImgService(request)
    else:
        pass
    return {"message": "Google Gemini endpoint"}