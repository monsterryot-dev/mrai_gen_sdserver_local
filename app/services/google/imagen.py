"""
Google Imagen 서비스 모듈
"""
from google.genai import types
from app.services.google.client import GoogleClient

from app.schemas.requests.google.imagen import ImagenRequestPost

from app.constants.messages.google import errorMessages
from app.constants.google import (
    imagenTokenCountModel, 
    imagenTokenLimit
)

class GoogleImagenService(GoogleClient):
    def __init__(self, requestBody: ImagenRequestPost):
        super().__init__(requestBody)

    def setApiPrams(self) -> dict[str, any]:
        if self.request is None:
            raise Exception(errorMessages["initError"].format(value="request"))
    
        request = self.request

        model = request.model
        prompt = request.prompt

        promptToken = self.getCountToken(model=imagenTokenCountModel, contents=prompt)
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