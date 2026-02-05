from typing import get_args
from fastapi import Form, File, UploadFile
from pydantic import BaseModel, Field, field_validator

from app.constants.model import GoogleNanoBananaModels
from app.constants.google import contentAspectRatioLiteral, contentImageSizeLiteral

class ImageToImageRequestBasie(BaseModel):
    model:GoogleNanoBananaModels = Field(
        ...,
        title="Nano Banana 모델명",
        description="사용할 Nano Banana 모델 이름"
    )
    prompt:str = Field(
        ...,
        title="이미지 생성 프롬프트",
        description="생성할 이미지에 대한 설명 텍스트"
    )
    image:bytes = Field(
        ...,
        title="입력 이미지 파일",
        description="이미지 변환에 사용할 입력 이미지 파일",
    ),
    temperature:float = Field(
        1.0,
        ge=0.0,
        le=1.0,
        title="샘플링 온도",
        description="답변의 창의성과 무작위성을 조절하는 값 (범위: 0.0~1.0)"
    ),
    candidateCount:int = Field(
        1,
        ge=1,
        le=4,
        title="생성할 이미지 수",
        description="생성할 이미지의 개수 (범위: 1~4)",
    )
    seed:int | None = Field(
        None,
        ge=0,
        le=2**32 - 1,
        title="랜덤 시드 값",
        description="이미지 생성 시 사용할 랜덤 시드 값 (0~4294967295 사이의 정수, None일 경우 무작위 시드 사용)",
    )
    aspectRatio:contentAspectRatioLiteral = Field(
        "1:1",
        title="이미지 가로세로 비율",
        description="생성할 이미지의 가로세로 비율 (가능한 값: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9)",
    )
    imageSize:contentImageSizeLiteral = Field(
        "1k",
        title="이미지 크기 [nano banana pro만 지원]",
        description="생성할 이미지의 크기 (가능한 값: 1k, 2k, 4k)",
    )

    @field_validator("model", mode="before")
    @classmethod
    def validateModel(cls, v):
        allowedNames = list(GoogleNanoBananaModels.__members__.keys())
        allowedValues = [m.value for m in GoogleNanoBananaModels]

        if isinstance(v, str):
            vUpper= v.upper().strip()

            if vUpper in allowedNames:
                return GoogleNanoBananaModels[vUpper]
            
            if v in allowedValues:
                return GoogleNanoBananaModels(v)
            
            raise ValueError(
                f"{allowedNames}, {allowedValues}"
            )
            
        raise ValueError(f"모델은 문자열이어야 합니다")
    
    @field_validator("seed", mode="before")
    @classmethod
    def validateSeed(cls, v):
        if v == "None":
            return None
        if v is None:
            return v
        if isinstance(v, int):
            return v
        raise ValueError("시드는 정수이거나 None이어야 합니다")
    
    @field_validator("imageSize", mode="before")
    @classmethod
    def validateImageSize(cls, v):
        v = v.lower().strip()

        validSizes = get_args(contentImageSizeLiteral)
        if v in validSizes:
            return v

        raise ValueError(
            f"{validSizes}"
        )

class ImageToImageRequestPost(ImageToImageRequestBasie):
    @classmethod
    def asForm(
        cls,
        model:str=Form(...),
        prompt:str=Form(...),
        temperature:float = Form(1.0, ge=0.0, le=1.0),
        candidateCount:int = Form(1, ge=1, le=4),
        seed:int | None = Form(None, ge=0, le=2**32 - 1),
        aspectRatio:str = Form("1:1"),
        imageSize:str = Form("1k"),
    ):
        return cls(
            model=model,
            prompt=prompt,
            temperature=temperature,
            candidateCount=candidateCount,
            seed=seed,
            aspectRatio=aspectRatio,
            imageSize=imageSize,
        )

    @classmethod
    def asFile(
        cls,
        image: UploadFile = File(...),
    ):
        return image