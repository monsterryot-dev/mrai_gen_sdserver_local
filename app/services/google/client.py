"""
Google API 클라이언트 서비스 모듈
"""
import datetime
from PIL import Image
from typing import Any
from google import genai

from app.core.settings import settings
from app.utils.file import checkAndCreateDir

class GoogleApiClient:
    def __init__(self):
        self.client: genai.Client = None
        self.apiKey: str = settings.googleapikey
        self.filePath: str = settings.imageFilePath

        # 출력 디렉토리 생성
        checkAndCreateDir(self.filePath)

    def setGoogleClient(self):
        self.client = genai.Client(api_key=self.apiKey)
        return self.client
    
    def getImageFormat(self, image):
        # Google genai API의 Image 객체인 경우
        if hasattr(image, 'mime_type'):
            return image.mime_type.split('/')[-1]
        
        # PIL Image 객체인 경우
        elif hasattr(image, 'format'):
            return (image.format or "png").lower()
        
        # 기본값
        return "png"

    def setFileName(self, prefix: str = "google_image", idx: int = None, format: str = "png"):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")

        format = format.lower()

        if idx is not None:
            return f"{prefix}_{timestamp}_{idx}.{format}"
        return f"{prefix}_{timestamp}.{format}"
        

    def makeImage(self, requestBody: Any):
        # 자식 클래스에서 구현
        pass
    
    def setParams(self, requestBody: Any):
        # 자식 클래스에서 구현
        pass
    
    def saveImage(self, images: Any):
        # 자식 클래스에서 구현
        pass