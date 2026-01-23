"""
라우터 로드 컨텍스트 매니저 데코레이터
"""
from contextlib import contextmanager

@contextmanager
def routerLoadContext(name:str):
    print(f"라우터 '{name}' 로드 중...")
    try:
        yield
    except Exception as e:
        print(f"라우터 '{name}' 로드 오류: {e}")
    finally:
        print(f"라우터 '{name}' 로드 완료.")

@contextmanager
def endpointContext():
    try:
        yield
    except Exception as e:
        print(f"라우터 컨텍스트 오류: {e}")
    finally:
        pass