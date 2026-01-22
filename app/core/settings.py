"""
FastAPI 애플리케이션 설정 정보
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    appName: str = "mrai_gen_sdserver_local"
    appVersion: str = "1.2.0"

settings = Settings()