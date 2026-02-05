"""
FastAPI 핸들러 설정
"""
from fastapi import FastAPI
from pydantic_core import ValidationError
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.schemas.responses.handler import ExceptionHandlerResponse

from app.constants.messages.handler import defaultMessage, handlerMessage

def settingHandlers(app: FastAPI) -> FastAPI:
    @app.exception_handler(StarletteHTTPException)
    async def httpExceptionHandler(request, exc):
        code = exc.status_code
        handlerResponse = ExceptionHandlerResponse(
            code=code,
            result=False,
            message=handlerMessage.get(code, defaultMessage)
        )
        return handlerResponse.setResponse()
    
    @app.exception_handler(Exception)
    async def generalExceptionHandler(request, exc):
        code = 500
        handlerResponse = ExceptionHandlerResponse(
            code=code,
            result=False,
            message=handlerMessage.get(code, defaultMessage)
        )
        return handlerResponse.setResponse()
    
    @app.exception_handler(RequestValidationError)
    async def validationExceptionHandler(request, exc):
        code = 422
        handlerResponse = ExceptionHandlerResponse(
            code=code,
            result=False,
            message=handlerMessage.get(code, defaultMessage),
            errors=exc.errors()
        )
        return handlerResponse.setResponse()
    
    @app.exception_handler(ValidationError)
    async def pydanticValidationExceptionHandler(request, exc):
        code = 422
        handlerResponse = ExceptionHandlerResponse(
            code=code,
            result=False,
            message=handlerMessage.get(code, defaultMessage),
            errors=exc.errors()
        )
        return handlerResponse.setResponse()
    
    return app