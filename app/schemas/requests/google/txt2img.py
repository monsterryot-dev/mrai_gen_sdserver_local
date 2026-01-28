from fastapi import Form
from typing import get_args
from pydantic import BaseModel, Field, field_validator

from app.constants.model import GoogleImagenModels
from app.constants.google import IMAGESIZE, OUTPUTMIMETYPE, ASPECTRATIO, PERSONGENERATION

class TextToImageRequestBasic(BaseModel):
    model:GoogleImagenModels = Field(
        ...,
        title="Imagen 모델명",
        description="사용할 Imagen 모델 이름"
    )
    prompt:str = Field(
        ...,
        title="이미지 생성 프롬프트",
        description="생성할 이미지에 대한 설명 텍스트"
    )
    numberOfImages:int = Field(
        1,
        ge=1,
        le=4,
        title="생성할 이미지 수",
        description="생성할 이미지의 개수 (범위: 1~4)",
    )
    imageSize:IMAGESIZE = Field(
        "1k",
        title="이미지 크기",
        description="생성할 이미지의 크기 (가능한 값: 1k, 2k)",
    )
    outputMimeType:OUTPUTMIMETYPE = Field(
        "image/png",
        title="출력 이미지 MIME 타입",
        description="생성할 이미지의 MIME 타입 (가능한 값: image/png, image/jpeg)",
    )
    aspectRatio:ASPECTRATIO = Field(
        "1:1",
        title="이미지 가로세로 비율",
        description="생성할 이미지의 가로세로 비율 (가능한 값: 1:1, 16:9, 9:16)",
    )
    personGeneration:PERSONGENERATION = Field(
        "allow_adult",
        title="사람 생성 옵션",
        description="이미지 내 사람 생성 옵션 (가능한 값: dont_allow, allow_adult, allow_all)",
    )
    guidanceScale:float = Field(
        7.5,
        ge=1.0,
        le=20.0,
        title="가이던스 스케일",
        description="이미지 생성 시 가이던스 스케일 값 (범위: 1.0~30.0)",
    )

    @field_validator("model", mode="before")
    @classmethod
    def validateModel(cls, v):
        allowedNames = list(GoogleImagenModels.__members__.keys())
        allowedValues = [m.value for m in GoogleImagenModels]

        if isinstance(v, str):
            vUpper= v.upper().strip()

            if vUpper in allowedNames:
                return GoogleImagenModels[vUpper]
            
            if v in allowedValues:
                return GoogleImagenModels(v)
            
            raise ValueError(
                f"{allowedNames}, {allowedValues}"
            )
            
        raise ValueError(f"모델은 문자열이어야 합니다")

    @field_validator("imageSize", mode="before")
    @classmethod
    def validateImageSize(cls, v):
        v = v.lower().strip()

        validSizes = get_args(IMAGESIZE)
        if v in validSizes:
            return v

        raise ValueError(
            f"{validSizes}"
        )

class TextToImageRequestPost(TextToImageRequestBasic):
    @classmethod
    def asForm(
        cls,
        model:str=Form(...),
        prompt:str=Form(...),
        numberOfImages:int = Form(1, ge=1, le=4),
        imageSize:str = Form("1k"),
        outputMimeType:str = Form("image/png"),
        aspectRatio:str = Form("1:1"),
        personGeneration:str = Form("allow_adult"),
        guidanceScale:float = Form(7.5, ge=1.0, le=20.0)
    ):
        return cls(
            model=model,
            prompt=prompt,
            numberOfImages=numberOfImages,
            imageSize=imageSize,
            outputMimeType=outputMimeType,
            aspectRatio=aspectRatio,
            personGeneration=personGeneration,
            guidanceScale=guidanceScale
        )