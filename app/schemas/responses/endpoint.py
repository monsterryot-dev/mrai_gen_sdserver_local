"""
라우터 엔드포인트 응답 스키마 정의
"""
from fastapi.responses import JSONResponse

class EndpointResponse:
    def __init__(self, result: bool, code: int, data: dict):
        self.result = result
        self.code = code
        self.data = data or {}

    def setResponse(self) -> JSONResponse:
        content = {
            "result": self.result,
            "code": self.code,
            "data": self.data
        }
        return JSONResponse(
            status_code=self.code,
            content=content
        )