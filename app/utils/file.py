"""
파일 관련 유틸리티 함수들
"""
import os

def checkAndCreateDir(directoryPath: str):
    """
    디렉토리가 존재하는지 확인하고, 없으면 생성합니다.
    """
    if not os.path.exists(directoryPath):
        os.makedirs(directoryPath)

def makeFileName(
        prefix: str, 
        extension: str, 
        idx:int=None,
        timestamp:str=None
    ) -> str:
    """
    파일 이름 생성
    """
    extension = extension.lower()
    fileName = prefix

    suffixes = [value for value in (idx, timestamp) if value is not None]
    if suffixes:
        fileName += "_" + "_".join(str(value) for value in suffixes)
    
    return f"{fileName}.{extension}"

def getFileExtension(fileName: str) -> str:
    """
    파일 이름에서 확장자 추출
    """
    return os.path.splitext(fileName)[1][1:].lower()  # 점(.) 제거

