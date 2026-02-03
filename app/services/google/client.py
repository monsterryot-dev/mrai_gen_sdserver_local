"""
Google API 클라이언트 서비스 모듈
"""
import re
import datetime
from google import genai
from google.genai import types
from typing import Any, Optional

from app.core.settings import settings
from app.utils.file import checkAndCreateDir

class GoogleApiClient:
    def __init__(self):
        self.__apiKey: str = settings.googleapikey
        self.client: genai.Client = None
        self.filePath: str = settings.imageFilePath

        # 출력 디렉토리 생성
        checkAndCreateDir(self.filePath)

    def __setGoogleClient(self) -> genai.Client:
        try:
            self.client = genai.Client(
                api_key=self.__apiKey,
                http_options=types.HttpOptions(
                    timeout=settings.googleTimeout
                )
            )
        except Exception as e:
            raise Exception(f"Google API 클라이언트 생성 실패: {str(e)}")
    
    def checkGoogleClient(self) -> None:
        if self.client is None:
            self.__setGoogleClient()
    
    def getModelList(
            self, 
            pattern:str = None, 
            ignoreCase:bool = True
        ) -> list[str]:
        # 패턴이 None이면 전체 모델 이름 리스트 반환
        # 예: imagen -> pattern = r"imagen"
        # 예: gemini 이미지 모델 -> pattern = r"^(?=.*gemini)(?=.*image).*$"
        if self.client is None:
            self.__setGoogleClient()

        modelList = self.client.models.list()
        names = [getattr(m, "name", "") for m in modelList]

        if not pattern:
            return names

        flags = re.IGNORECASE if ignoreCase else 0
        regex = re.compile(pattern, flags)

        return [name for name in names if regex.search(name)]
        
    def getCountToken(
            self, 
            model:str,
            contents: Optional[str|list]
        ) -> dict[str, int]:
        if self.client is None:
            self.__setGoogleClient()

        tokenClass = self.client.models.count_tokens(
            model=model,
            contents=contents
        )
        tokenDict = tokenClass.__dict__

        return {
            'totalToken': tokenDict.get('total_tokens', 0),
            'cachedContentTokenCount': tokenDict.get('cached_content_token_count', 0),
        }
    
    def getModelMaxToken():
        # TODO: 모델별 최대 토큰 수 반환 함수 구현
        pass
            
    def getImageFormat(self, image: Any) -> str:
        # Google genai API의 Image 객체인 경우
        if hasattr(image, 'mime_type'):
            return image.mime_type.split('/')[-1]
        
        # PIL Image 객체인 경우
        elif hasattr(image, 'format'):
            return (image.format or "png").lower()
        
        # 기본값
        return "png"

    def setFileName(
            self, 
            idx: int = None, 
            prefix: str = "google_image", 
            format: str = "png"
        ) -> str:
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