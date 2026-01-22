"""
FastAPI 핸들러 설정
"""
from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.responses.handler import ExceptionHandlerResponse

from app.constants.handler import handlerMessage

def settingHandlers(app: FastAPI) -> FastAPI:
    @app.exception_handler(StarletteHTTPException)
    async def httpExceptionHandler(request, exc):
        code = exc.status_code
        handlerResponse = ExceptionHandlerResponse(
            code=code,
            result=False,
            message=handlerMessage.get(code, "알 수 없는 오류가 발생했습니다.")
        )
        return handlerResponse.setResponse()
    
    @app.exception_handler(Exception)
    async def generalExceptionHandler(request, exc):
        code = 500
        handlerResponse = ExceptionHandlerResponse(
            code=code,
            result=False,
            message=handlerMessage.get(code, "알 수 없는 오류가 발생했습니다.")
        )
        return handlerResponse.setResponse()
    return app