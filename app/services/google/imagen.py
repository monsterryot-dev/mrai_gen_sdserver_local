"""
google imagen 서비스를 이용한 이미지 생성 서비스 모듈
"""
import os
from PIL import Image
from google.genai import types

from app.services.google.client import GoogleApiClient
from app.schemas.requests.google.imagen import ImagenRequestPost

class GoogleImagenService(GoogleApiClient):
    def makeImage(self, requestBody: ImagenRequestPost):
        client = self.setGoogleClient()

        params = self.setParams(requestBody)

        clientResponse = client.models.generate_images(
            model=params["model"],
            prompt=params["prompt"],
            config=params["config"],
        )

        images = self.saveImage(clientResponse.generated_images, 'generated_imagen')

        return {"imageList": images}
    
    def setParams(self, requestBody: ImagenRequestPost):
        model = requestBody.model

        prompt = requestBody.prompt

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
    
    def saveImage(self, images: list[Image.Image], fileNamePrefix: str = "generated_imagen"):
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