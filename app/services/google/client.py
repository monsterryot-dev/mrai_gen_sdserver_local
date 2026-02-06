"""
Google 클라이언트 서비스 모듈
"""
import re
from google import genai
from typing import Optional

from app.core.settings import settings
from app.utils.file import checkAndCreateDir

from app.constants.messages.google import errorMessages

class GoogleClient:
    """
    google api의 client를 생성 관리하는 클래스
    """
    def __init__(self, requestBody: Optional[any] = None):
        self.__apiKey: str = settings.googleapikey
        self.filePath: str = settings.imageFilePath
        self.client: genai.Client = None
        
        checkAndCreateDir(self.filePath)

    def __setGoogleClient(self) -> None:
        try:
            self.client = genai.Client(
                api_key=self.__apiKey,
                http_options=genai.types.HttpOptions(
                    timeout=settings.googleTimeout
                )
            )
        except Exception as e:
            raise Exception(errorMessages["clientError"].format(errorDetail=str(e)))
    
    def checkClient(self) -> None:
        """
        client가 None이면 새로 생성
        """
        if self.client is None:
            self.__setGoogleClient()
        
    def getModelList(
            self,
            pattern:str = None,
            ignoreCase:bool = True
        ) -> list[str]:
        """
        INFO: 실 운영에서는 사용 안함
        패턴이 None이면 전체 모델 이름 리스트 반환
        예: imagen -> pattern = r"imagen"
        예: gemini 이미지 모델 -> pattern = r"^(?=.*gemini)(?=.*image).*$"
        """
        self.checkClient()

        modelList = self.client.models.list()
        names = [getattr(m, "name", "") for m in modelList]

        if not pattern:
            return names
        
        flags = re.IGNORECASE if ignoreCase else 0
        regex = re.compile(pattern, flags)
        return [name for name in names if regex.search(name)]

    def countTokens(self, model:str, contents:Optional[str|list]) -> dict[str, int]:
        """
        주어진 모델과 프롬프트에 대한 토큰 수 계산
        """
        self.checkClient()
        tokenCount = self.client.models.count_tokens(
            model=model,
            contents=contents
        ).__dict__

        return {
            "totalTokens": tokenCount.get("total_tokens", 0),
            "cachedContentTokenCount": tokenCount.get("cached_content_token_count", 0),
        }
    
    def getTokenLimit(self, model:str) -> int:
        """
        주어진 모델의 토큰 한도 반환
        """
        self.checkClient()
        modelInfo = self.client.models.get(model=model)

        if hasattr(modelInfo, 'input_token_limit'):
            return modelInfo.input_token_limit
        
        return 0
    
    def setApiParams(self, request:any) -> dict[str, any]:
        """
        자식 클래스에서 오버라이드하여 API 호출에 필요한 파라미터 설정
        """
        pass

    def runApi(self, parameters:dict[str, any]) -> any:
        """
        자식 클래스에서 오버라이드하여 API 호출 실행
        """
        pass

    def setResult(self, response:any) -> dict[str, any]:
        """
        자식 클래스에서 오버라이드하여 API 호출 결과 설정
        """
        pass

    def setResultImage(self, images:any) -> list[str]:
        """
        자식 클래스에서 오버라이드하여 이미지 결과 저장 및 반환
        """
        pass