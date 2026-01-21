from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    appName: str = "mrai_gen_sdserver_local"
    appVersion: str = "1.2.0"

settings = Settings()