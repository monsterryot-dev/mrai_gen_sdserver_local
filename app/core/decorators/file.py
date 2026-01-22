"""
파일 관련 컨텍스트 매니저 데코레이터
"""
from contextlib import contextmanager

@contextmanager
def fileContext(filePath, mode):
    f = open(filePath, mode)
    try:
        yield f
    except Exception as e:
        print(f"File Error: {e}")
    finally:
        f.close()
    