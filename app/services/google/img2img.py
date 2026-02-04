"""
google 서비스를 이용한 이미지 생성 서비스 모듈
"""
import os
from PIL import Image
from google.genai import types

from app.services.google.client import GoogleApiClient
from app.schemas.requests.google.img2img import ImageToImageRequestPost

from app.constants.google import DEFAULTSAFEERRORMESSAGE, CONTENTNAMERPREFIX

class GoogleImg2ImgService(GoogleApiClient):
    def __init__(self, image: bytes):
        super().__init__()
        self.image = self.loadImage(image)

    def makeImage(
            self, 
            requestBody: ImageToImageRequestPost,
        ) -> dict[str, list[str]]:
        self.checkGoogleClient()

        params = self.setParams(requestBody)

        clientResponse = self.client.models.generate_content(
            model=params["model"],
            contents=[params["prompt"], self.image],
            config=params["config"],
        )

        result = self.setImageResult(clientResponse, CONTENTNAMERPREFIX)

        return result
    
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
        tokenLimitInfo = self.getModelMaxToken(model=model)

        if tokenInfo['totalToken'] > tokenLimitInfo['inputTokenLimit']:
            raise Exception(f"프롬프트가 너무 깁니다. {tokenLimitInfo['inputTokenLimit']} 토큰 이하로 줄여주세요.")

        imageConfig=types.ImageConfig(
            aspect_ratio=requestBody.aspectRatio,
            image_size=requestBody.imageSize if "PRO" in model.name else None,
        )
        
        config = types.GenerateContentConfig(
            response_modalities=["image"],
            temperature=requestBody.temperature,
            candidate_count=requestBody.candidateCount,
            seed=requestBody.seed,
            image_config=imageConfig,
        )
        
        return {
            "model": model,
            "prompt": prompt,
            "config": config,
        }

    def setImageResult(
            self, 
            response: types.GenerateContentResponse,
            fileNamePrefix: str = CONTENTNAMERPREFIX
        ) -> list[str]:

        partList = []
        
        if not response.candidates:
            return {
                "partList": [], 
                "message": DEFAULTSAFEERRORMESSAGE
            }
     
        for part in response.parts:
            if part.text is not None:
                partList.append({
                    "type": "text",
                    "content": part.text
                })
            elif image:=part.as_image():
                imagePath = self.saveImage(image, fileNamePrefix)
                partList.append({
                    "type": "image",
                    "content": imagePath
                })
        
        return {
            "partList": partList
        }
    
    def saveImage(
        self,
        imageData: Image.Image,
        fileNamePrefix: str = CONTENTNAMERPREFIX
    ) -> str:
        format = self.getImageFormat(imageData)
        fileName = self.setFileName(prefix=fileNamePrefix, idx=0, format=format)
        filePath = os.path.join(self.filePath, fileName)

        imageData.save(filePath)
        return filePath