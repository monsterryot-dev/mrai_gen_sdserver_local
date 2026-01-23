"""
Google API 클라이언트 서비스 모듈
"""
from google import genai
from google.genai import types

from app.core.settings import settings

class GoogleApiClient:
    apiKey: str = settings.googleApiKey
    client: genai.Client = None

    def setGoogleClient(self):
        self.client = genai.Client(api_key=self.apiKey)

    def makeImiage():
        # 자식 클래스에서 구현
        pass
    
    def saveImage():
        # 자식 클래스에서 구현
        pass
