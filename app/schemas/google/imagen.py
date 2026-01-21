# TODO: form 코드 정리 중
from fastapi import Form
from typing import get_args
from pydantic import BaseModel, Field, field_validator

from app.constants.model import GoogleImagenModels
from app.constants.google import IMAGESIZE

class ImagenRequestBasic(BaseModel):
    model:GoogleImagenModels = Field(
        ...,
        title="Imagen 모델명",
        description="사용할 Imagen 모델 이름"
    )
    numberOfImages:int = Field(
        1,
        ge=1,
        le=4,
        title="생성할 이미지 수",
        description="생성할 이미지 수 옵션값 [범위: 1~4]"
    )
    imageSize:str = Field(
        "1k",
        title="생성할 이미지 해상도",
        description=f"생성할 이미지 해상도 옵션값 [가능값: {IMAGESIZE}]",
    )

    # 모델 ENUM의 KEY를 받아서 VALUE로 변환
    @field_validator("model", mode="before")
    @classmethod
    def validateModel(cls, v):
        try:
            if GoogleImagenModels[v]:
                return GoogleImagenModels[v]
        except Exception:
            return GoogleImagenModels(v)

    # imageSize가 지정된 옵션값인지 검증
    @field_validator("imageSize", mode="before")
    @classmethod
    def validateImageSize(cls, v):
        v = v.lower()
        if v in get_args(IMAGESIZE):
            return v
        else:
            raise ValueError(f"imageSize 옵션값 오류: {v} (가능값: {IMAGESIZE})")

class ImagenRequestPost(ImagenRequestBasic):
    def __call__(self, *args, **kwds):
        return super().__call__(*args, **kwds)
    
    @classmethod
    def asForm(
        cla,
        model:GoogleImagenModels=Form(
            ...,
            title="Imagen 모델명",
            description="사용할 Imagen 모델 이름"
        ),
        numberOfImages:int=Form(
            1,
            ge=1,
            le=4,
            title="생성할 이미지 수",
            description="생성할 이미지 수 옵션값 [범위: 1~4]"
        ),
        imageSize:str=Form(
            "1k",
            title="생성할 이미지 해상도",
            description=f"생성할 이미지 해상도 옵션값 [가능값: {IMAGESIZE}]"
        ),
    ):
        return cla(
            model=model,
            numberOfImages=numberOfImages,
            imageSize=imageSize
        )
        