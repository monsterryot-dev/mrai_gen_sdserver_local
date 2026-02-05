"""
라우터 로드 컨텍스트 매니저 데코레이터
"""
from functools import wraps
from contextlib import contextmanager

from app.core.logger import logger
from app.schemas.responses.endpoint import EndpointResponse

from app.constants.messages import routerLoadMessage, endpointMessage

@contextmanager
def routerLoadContext(name:str):
    logger.writeLog(level="info", message=routerLoadMessage["start"].format(name=name))
    try:
        yield
    except Exception as e:
        logger.writeLog(level="error", message=routerLoadMessage["error"].format(name=name, error=e))
    finally:
        logger.writeLog(level="info", message=routerLoadMessage["complete"].format(name=name))

def endpointContext(function):
    """커스텀 엔드포인트 데코레이터"""
    @wraps(function)
    async def async_wrapper(*args, **kwargs):
        try:
            result = await function(*args, **kwargs)
            logger.writeLog(level="info", message=endpointMessage["success"].format(function=function.__name__))
            return EndpointResponse(
                result=True,
                code=200,
                data=result
            ).setResponse()
        
        except Exception as e:
            logger.writeLog(level="error", message=endpointMessage["error"].format(error=e))
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
    