"""
Google Imagen 서비스 모듈
"""
import os
from PIL import Image
from datetime import datetime
from google.genai import types
from app.services.google.client import GoogleClient
from app.utils.file import makeFileName, getFirstFileInDir

from app.schemas.requests.google.imagen import ImagenRequestPost

from app.constants.messages.google import errorMessages
from app.constants.google import (
    imagenTokenCountModel, 
    imagenTokenLimit,
    imagenImageNamePrefix
)

def googleImagenTestService():
    """
    Google Imagen 테스트 서비스 함수
    """
    from app.core.settings import settings
    imagePath = settings.imageFilePath

    imageFile = getFirstFileInDir(
        directoryPath=imagePath,
        extensions=["*.png", "*.jpg", "*.jpeg"]
    )
    
    if imageFile is None:
        return {
            "imageList": [], 
            "message": errorMessages["noImageError"].format(imagePath=imagePath, extension="png/jpg/jpeg")
        }
    else:
        return  {"imageList": [imageFile]}

def googleImagenService(request: ImagenRequestPost):
    """
    Google Imagen 서비스 생성 함수
    """
    service = GoogleImagen()

    prams = service.setApiPrams(request)

    response = service.runApi(prams)

    result = service.setResult(response)

    return result

class GoogleImagen(GoogleClient):
    """
    Google Imagen 서비스 클래스
    """
    def __init__(self):
        super().__init__()

    def setApiPrams(self, request: ImagenRequestPost) -> dict[str, any]:
        model = request.model
        prompt = request.prompt

        promptToken = self.countTokens(model=imagenTokenCountModel, contents=prompt)['totalTokens']
        if promptToken > imagenTokenLimit:
            raise Exception(errorMessages["promptTokenLimitError"].format(tokenLimit=imagenTokenLimit))

        config = types.GenerateImagesConfig(
            number_of_images=request.numberOfImages,
            image_size=request.imageSize,
            output_mime_type=request.outputMimeType,
            aspect_ratio=request.aspectRatio,
            person_generation=request.personGeneration,
            guidance_scale=request.guidanceScale,
        )
        
        return {
            "model": model,
            "prompt": prompt,
            "config": config,
        }
    
    def runApi(self, parameters:dict[str, any]) -> types.GenerateImagesResponse:
        self.checkClient()

        clientResponse  = self.client.models.generate_images(
            model=parameters["model"],
            prompt=parameters["prompt"],
            config=parameters["config"],
        )
        
        return clientResponse
    
    def setResult(self, response: types.GenerateImagesResponse) -> dict[str, list[str]]:
        images = getattr(response, "generated_images", None)
        if not images:
            return {
                "imageList": [], 
                "message": errorMessages["noImageError"]
            }

        return {
            "imageList": self.setResultImage(images)
        }
    
    def setResultImage(self, images:list[types.GeneratedImage]) -> list[str]:
        returnList = []
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        for idx, image in enumerate(images):
            if not isinstance(image, Image.Image):
                image = image.image
            extension = image.mime_type.split('/')[-1]
            fileName = makeFileName(
                prefix=imagenImageNamePrefix,
                idx=idx,
                extension=extension,
                timestamp=timestamp
            )
            filePath = os.path.join(self.filePath, fileName)

            image.save(filePath)
            returnList.append(filePath)

        return returnList
