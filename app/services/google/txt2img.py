"""
google 서비스를 이용한 이미지 생성 서비스 모듈
TODO: google class uml 나머지 정리 및 문서화 후 노션에 추가
"""
import os
from PIL import Image
from google.genai import types

from app.services.google.client import GoogleApiClient
from app.schemas.requests.google.txt2img import TextToImageRequestPost

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

        images = self.saveImage(clientResponse.generated_images, 'generated_imagen')

        return {"imageList": images}
    
    def setParams(
            self, 
            requestBody: TextToImageRequestPost
        ) -> dict[str, any]:
        model = requestBody.model

        # INFO: 현재는 Imagen v4를 지원하지 않아서 gemini-2.0-flash 모델로 계산함
        prompt = requestBody.prompt
        tokenInfo = self.getCountToken(
            model="models/gemini-2.0-flash",
            contents=prompt
        )

        if int(tokenInfo['totalToken']) > 480:
            raise Exception("프롬프트가 너무 깁니다. 480 토큰 이하로 줄여주세요.")

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
    
    def saveImage(
            self, 
            images: list[Image.Image], 
            fileNamePrefix: str = "generated_imagen"
        ) -> list[str]:
        savedImagePaths = []
        for idx, imageData in enumerate(images):
            if not isinstance(imageData, Image.Image):
                imageData = imageData.image

            format = self.getImageFormat(imageData)
            fileName = self.setFileName(prefix=fileNamePrefix, idx=idx, format=format)
            filePath = os.path.join(self.filePath, fileName)

            imageData.save(filePath)
            savedImagePaths.append(filePath)
        return savedImagePaths