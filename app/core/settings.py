"""
FastAPI 애플리케이션 설정 정보
"""
import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )
    appName: str = "mrai_gen_sdserver_local"
    appVersion: str = "1.2.0"

    googleTimeout: int = 60 * 1000 # milliseconds [60초]

    # BUILD: 실제 배포 시에는 False로 변경 필요
    debug: bool = True
    logFormat: str = "[%(asctime)s] %(levelname)s: %(message)s"

    basicPath: str = os.getcwd()
    homePath: str = str(Path.home())
    logFilePath: str = os.path.join(os.getcwd(), "logs")
    imageFilePath: str = os.path.join(homePath, "Documents", "MRAI Desktop", "output")

settings = Settings()