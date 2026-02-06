"""
google gemini 관련 라우터 모듈
"""
from typing import Optional
from fastapi import APIRouter, Depends

from app.core.decorators.exception import endpointContext

from app.schemas.requests.google.gemini.generate import (
    GeminiGenerateRequestPost
)

geminiRouter = APIRouter()

@geminiRouter.post("/")
@endpointContext
async def generateGoogleGemini(
    request: GeminiGenerateRequestPost = Depends(GeminiGenerateRequestPost.asForm),
):
    # print(image)
    return {"message": "Google Gemini endpoint"}