"""
FastAPI 애플리케이션 설정 정보
"""
import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )
    
    appName: str = "mrai_gen_sdserver_local"
    appVersion: str = "1.2.0"

settings = Settings()