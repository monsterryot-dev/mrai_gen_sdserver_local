"""
google gemini 관련 라우터 모듈
"""
from fastapi import APIRouter, Depends

from app.core.decorators.exception import endpointContext

geminiRouter = APIRouter()

# @geminiRouter.post("")