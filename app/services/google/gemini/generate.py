"""
Google Gemini 이미지 생성 서비스 모듈
"""
import os
from PIL import Image
from datetime import datetime
from google.genai import types

from app.services.google.client import GoogleClient
from app.utils.file import makeFileName, getFirstFileInDir

from app.schemas.requests.google.gemini.generate import GeminiGenerateRequestPost

from app.constants.messages.google import errorMessages
from app.constants.google import geminiImageNamePrefix, geminiImageExtension

def googleGeminiTestService():
    """
    Google Gemini 테스트 서비스 함수
    """
    return {"message": "Google Gemini test service"}

def googleGeminiTxt2ImgService(request: GeminiGenerateRequestPost):
    """
    Google Gemini txt2img 생성 서비스 함수
    """
    service = GoogleGeminiGenerateTxt2Img()

    params = service.setApiParams(request)
    params["contents"] = [params["prompt"]]

    response = service.runApi(params)

    result = service.setResult(response)

    return result

class GoogleGeminiGenerateBasic(GoogleClient):
    """
    Google Gemini 이미지 생성 서비스 클래스
    """
    def __init__(self):
        super().__init__()

    def setApiParams(self, request:GeminiGenerateRequestPost):
        model = request.model
        prompt = request.prompt

        promptToken = self.countTokens(model=model, contents=prompt)['totalTokens']
        geminiTokenLimitInfo = self.getTokenLimit(model=model)
        if promptToken > geminiTokenLimitInfo:
            raise Exception(errorMessages["promptTokenLimitError"].format(tokenLimit=geminiTokenLimitInfo))
        
        imageConfig = types.ImageConfig(
            aspect_ratio=request.aspectRatio,
            image_size=request.imageSize if "PRO" in model.name else None,
        )

        config = types.GenerateContentConfig(
            response_modalities=["image"],
            temperature=request.temperature,
            candidate_count=request.candidateCount,
            seed=request.seed,
            image_config=imageConfig,
        )

        return {
            "model": model,
            "prompt": prompt,
            "config": config,
        }
    
    def runApi(self, parameters:dict[str, any]) -> types.GenerateContentResponse:
        self.checkClient()

        clientResponse  = self.client.models.generate_content(
            model=parameters["model"],
            contents=parameters["contents"],
            config=parameters["config"],
        )
        
        return clientResponse
    
    def setResult(self, response: types.GenerateContentResponse) -> dict[str, list[str]]:
        parts = response.parts
        if not parts:
            return {
                "imageList": [], 
                "message": errorMessages["noImageError"]
            }

        return {
            "imageList": self.setResultImage(parts),
        }

    def setResultImage(self, images: list[types.Candidate]) -> list[str]:
        returnList = []
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        idx = 0
        for part in images:
            if part.text is not None:
                continue
            elif part.inline_data is not None:
                image = part.as_image()

                fileName = makeFileName(
                    prefix=geminiImageNamePrefix,
                    idx=idx,
                    extension=geminiImageExtension,
                    timestamp=timestamp
                )
                filePath = os.path.join(self.filePath, fileName)
                image.save(filePath)
                returnList.append(filePath)
                idx += 1
        return returnList
    
class GoogleGeminiGenerateTxt2Img(GoogleGeminiGenerateBasic):
    """
    Google Gemini txt2img 생성 서비스 클래스
    """
    def __init__(self):
        super().__init__()

class GoogleGeminiGenerateImg2Img(GoogleGeminiGenerateBasic):
    """
    Google Gemini img2img 생성 서비스 클래스
    """
    def __init__(self):
        super().__init__()
