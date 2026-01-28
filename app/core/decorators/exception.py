"""
라우터 로드 컨텍스트 매니저 데코레이터
"""
from functools import wraps
from contextlib import contextmanager

from app.core.logger import logger
from app.schemas.responses.endpoint import EndpointResponse

@contextmanager
def routerLoadContext(name:str):
    logger.writeLog(level="info", message=f"라우터 '{name}' 로드 중...")
    try:
        yield
    except Exception as e:
        logger.writeLog(level="error", message=f"라우터 '{name}' 로드 오류: {e}")
    finally:
        logger.writeLog(level="info", message=f"라우터 '{name}' 로드 완료.")

def endpointContext(function):
    """커스텀 엔드포인트 데코레이터"""
    @wraps(function)
    async def async_wrapper(*args, **kwargs):
        try:
            result = await function(*args, **kwargs)
            logger.writeLog(level="info", message=f"엔드포인트 실행 성공: {function.__name__}")
            return EndpointResponse(
                result=True,
                code=200,
                data=result
            ).setResponse()
        
        except Exception as e:
            logger.writeLog(level="error", message=f'엔드포인트 에러: {e}')
            code = e.code if hasattr(e, 'code') else 500
            message = e.message if hasattr(e, 'message') else "Internal Server Error"

            return EndpointResponse(
                result=False,
                code=code,
                data={
                    "message": message
                }
            ).setResponse()
    return async_wrapper
    