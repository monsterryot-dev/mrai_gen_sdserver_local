# TODO: validation 로직 수정 및 정리 필요
from fastapi import Form
from typing import get_args
from pydantic import BaseModel, Field, field_validator

from app.constants.model import GoogleImagenModels
from app.constants.google import IMAGESIZE, ASPECTRATIO, PERSONGENERATION

class ImagenRequestBasic(BaseModel):
    model:GoogleImagenModels = Field(
        ...,
        title="Imagen 모델명",
        description="사용할 Imagen 모델 이름"
    )
    numberOfImages:int = Field(
        1,
        title="생성할 이미지 수",
        description="생성할 이미지의 개수 (범위: 1~4)",
        ge=1,
        le=4
    )
    imageSize:IMAGESIZE = Field(
        "1k",
        title="이미지 크기",
        description="생성할 이미지의 크기 (가능한 값: 1k, 2k)",
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
        title="가이던스 스케일",
        description="이미지 생성 시 가이던스 스케일 값 (범위: 1.0~20.0)",
        ge=1.0,
        le=20.0
    )

    @field_validator("model", mode="before")
    @classmethod
    def validateModel(cls, v):
        if isinstance(v, GoogleImagenModels):
            return v

        if isinstance(v, str):
            v = v.upper()
            if v in GoogleImagenModels.__members__:
                return GoogleImagenModels[v]
            else:
                return GoogleImagenModels(v)
            
        raise ValueError(
            f"모델명은 {list(GoogleImagenModels.__members__.keys())} "
            f"또는 { [m.value for m in GoogleImagenModels] } 중 하나여야 합니다"
        )

    @field_validator("imageSize", mode="before")
    @classmethod
    def validateImageSize(cls, v):
        v = v.lower()

        if v in get_args(IMAGESIZE):
            return v

        raise ValueError(
            f"imageSize는 {list(IMAGESIZE.__members__.keys())} "
            f"또는 { [s.value for s in IMAGESIZE] } 중 하나여야 합니다"
        )

class ImagenRequestPost(ImagenRequestBasic):
    def __call__(self, *args, **kwds):
        return super().__call__(*args, **kwds)
    
    @classmethod
    def asForm(
        cls,
        model=Form(
            ...,
            title="Imagen 모델명",
            description="사용할 Imagen 모델 이름",
            
        ),
        numberOfImages:int = Form(
            1,
            title="생성할 이미지 수",
            description="생성할 이미지의 개수 (범위: 1~4)",
            ge=1,
            le=4
        ),
        imageSize = Form(
            "1k",
            title="이미지 크기",
            description="생성할 이미지의 크기 (가능한 값: 1k, 2k)",
        ),
        aspectRatio:ASPECTRATIO = Form(
            "1:1",
            title="이미지 가로세로 비율",
            description="생성할 이미지의 가로세로 비율 (가능한 값: 1:1, 16:9, 9:16)",
        ),
        personGeneration:PERSONGENERATION = Form(
            "allow_adult",
            title="사람 생성 옵션",
            description="이미지 내 사람 생성 옵션 (가능한 값: dont_allow, allow_adult, allow_all)",
        ),
        guidanceScale:float = Form(
            7.5,
            title="가이던스 스케일",
            description="이미지 생성 시 가이던스 스케일 값 (범위: 1.0~20.0)",
            ge=1.0,
            le=20.0
        )
    ):
        return cls(
            model=model,
            numberOfImages=numberOfImages,
            imageSize=imageSize,
            aspectRatio=aspectRatio,
            personGeneration=personGeneration,
            guidanceScale=guidanceScale
        )