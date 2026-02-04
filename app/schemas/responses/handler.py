"""
오류 응답 스키마 정의
"""
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any

from app.constants.handler import validationMessage

class ExceptionHandlerResponse:
    def __init__(
            self, 
            result:bool, 
            code:int, 
            message:str,
            errors: Optional[List[Dict[str, Any]]] = None
        ):
        self.result = result
        self.code = code
        self.message = message
        self.errors = errors

    def setResponse(self) -> JSONResponse:
        message = self.message
        content = {
            "result": self.result,
            "code": self.code,
            "data": {
                "message": message if not self.errors else self._formatErrors(message)
            }
        }
        
        return JSONResponse(
            status_code=self.code, 
            content=content
        )

    def _formatErrors(self, defulatMessage:str) -> List[Dict[str, Any]]:
        """ValidationError를 사용자 친화적인 형식으로 변환"""
        for error in self.errors:
            errorType = error.get("type", "")
            key = error.get("loc", [""])[-1]
            allowed = error.get("ctx", {}).get("error", [])
            message = self._errorMessageFormat(errorType, key=key, allowed=allowed)
        return message
    
    def _errorMessageFormat(self, type:str, **kwargs) -> str:
        """오류 메시지 포맷팅"""
        message = validationMessage[type].format(**kwargs)
        return message