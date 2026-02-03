"""
google 서비스를 이용한 이미지 생성 서비스 모듈
"""
from app.services.google.client import GoogleApiClient
from app.schemas.requests.google.img2img import ImageToImageRequestPost

class GoogleImg2ImgService(GoogleApiClient):
    def __init__(self, image: bytes):
        super().__init__()
        self.image = image

    def makeImage(
            self, 
            requestBody: ImageToImageRequestPost,
        ) -> dict[str, list[str]]:
        self.checkGoogleClient()

        params = self.setParams(requestBody)
        return {"message": "이미지 생성 작업 중입니다."}

    def setParams(
            self, 
            requestBody: ImageToImageRequestPost,
        ) -> dict[str, any]:
        model = requestBody.model

        prompt = requestBody.prompt
        tokenInfo = self.getCountToken(
            model=model,
            contents=prompt
        )
        

        return {"message": "파라미터 설정 작업 중입니다."}

    def saveImage(
            self, 
            images: any,
            fileNamePrefix: str = "generated_nano_banana"
        ) -> list[str]:
        return {"message": "이미지 저장 작업 중입니다."}