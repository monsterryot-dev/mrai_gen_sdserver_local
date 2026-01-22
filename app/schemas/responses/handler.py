"""
오류 응답 스키마 정의
"""
import json
from fastapi.responses import JSONResponse

class ExceptionHandlerResponse:
    def __init__(self, result:bool, code:int, message:str):
        self.result = result
        self.code = code
        self.message = message

    def  setResponse(self) -> JSONResponse:
        content = {
            "result": self.result,
            "code": self.code,
            "message": self.message
        }
        return JSONResponse(
            status_code=self.code, 
            content=content
        )