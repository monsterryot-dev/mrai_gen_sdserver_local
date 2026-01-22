"""
서버 설정 정보를 불러오는 유틸리티 함수
"""
import json

from app.core.decorators.file import fileContext

def getServerInfo():
    with fileContext("server.json", "r") as f:
        config = json.load(f)
    return config