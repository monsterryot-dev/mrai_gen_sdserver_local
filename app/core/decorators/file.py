"""
파일 관련 컨텍스트 매니저 데코레이터
"""
from contextlib import contextmanager

from app.core.logger import logger

@contextmanager
def fileContext(filePath, mode):
    f = open(filePath, mode)
    try:
        yield f
    except Exception as e:
        logger.writeLog("error", f"파일 오류: {e}")
    finally:
        f.close()
    