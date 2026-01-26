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