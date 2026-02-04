"""
google 서비스를 이용한 이미지 생성 서비스 모듈
TODO: google class uml 나머지 정리 및 문서화 후 노션에 추가
"""
import os
from PIL import Image
from google.genai import types

from app.services.google.client import GoogleApiClient
from app.schemas.requests.google.txt2img import TextToImageRequestPost

from app.constants.google import DEFAULTSAFEERRORMESSAGE, IMAGENTOKENFINDMODEL, IMAGENINPUTTOKENLIMIT, IMAGENNAMEPREFIX

class GoogleTxt2ImgService(GoogleApiClient):
    def __init__(self):
        super().__init__()

    def makeImage(
            self, 
            requestBody: TextToImageRequestPost
        ) -> dict[str, list[str]]:
        self.checkGoogleClient()

        params = self.setParams(requestBody)

        clientResponse = self.client.models.generate_images(
            model=params["model"],
            prompt=params["prompt"],
            config=params["config"],
        )

        result = self.setImageResult(clientResponse, IMAGENNAMEPREFIX)

        return result
    
    def setParams(
            self, 
            requestBody: TextToImageRequestPost
        ) -> dict[str, any]:
        model = requestBody.model

        # INFO: 현재는 Imagen v4를 지원하지 않아서 gemini-2.0-flash 모델로 계산함
        prompt = requestBody.prompt
        tokenInfo = self.getCountToken(
            model=IMAGENTOKENFINDMODEL,
            contents=prompt
        )

        if int(tokenInfo['totalToken']) > IMAGENINPUTTOKENLIMIT:
            raise Exception(f"프롬프트가 너무 깁니다. {IMAGENINPUTTOKENLIMIT} 토큰 이하로 줄여주세요.")

        config = types.GenerateImagesConfig(
            number_of_images=requestBody.numberOfImages,
            image_size=requestBody.imageSize,
            output_mime_type=requestBody.outputMimeType,
            aspect_ratio=requestBody.aspectRatio,
            person_generation=requestBody.personGeneration,
            guidance_scale=requestBody.guidanceScale,
        )

        return {
            "model": model,
            "prompt": prompt,
            "config": config,
        }
    
    def setImageResult(
            self, 
            response: types.GenerateImagesResponse, 
            fileNamePrefix: str = IMAGENNAMEPREFIX
        ) -> list[str]:
        
        if not response.generated_images:
            return {
                "imageList": [], 
                "message": DEFAULTSAFEERRORMESSAGE
            }

        images = response.generated_images

        imageList = self.saveImage(images, fileNamePrefix)

        return {
            "imageList": imageList
        }

    def saveImage(
            self, 
            images: list[Image.Image], 
            fileNamePrefix: str = IMAGENNAMEPREFIX
        ) -> dict[str, list[str]]: 
            saveImagePath = []
            for idx, imageData in enumerate(images):
                if not isinstance(imageData, Image.Image):
                    imageData = imageData.image

                format = self.getImageFormat(imageData)
                fileName = self.setFileName(prefix=fileNamePrefix, idx=idx, format=format)
                filePath = os.path.join(self.filePath, fileName)

                imageData.save(filePath)
                saveImagePath.append(filePath)
            return saveImagePath