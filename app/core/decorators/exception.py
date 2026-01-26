"""
라우터 로드 컨텍스트 매니저 데코레이터
"""
from functools import wraps
from contextlib import contextmanager

from app.schemas.responses.endpoint import EndpointResponse

@contextmanager
def routerLoadContext(name:str):
    print(f"라우터 '{name}' 로드 중...")
    try:
        yield
    except Exception as e:
        print(f"라우터 '{name}' 로드 오류: {e}")
    finally:
        print(f"라우터 '{name}' 로드 완료.")

def endpointContext(function):
    """커스텀 엔드포인트 데코레이터"""
    @wraps(function)
    async def async_wrapper(*args, **kwargs):
        try:
            result = await function(*args, **kwargs)
            
            return EndpointResponse(
                result=True,
                code=200,
                data=result
            ).setResponse()
        
        except Exception as e:
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
    