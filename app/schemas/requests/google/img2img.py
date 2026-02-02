from typing import get_args
from fastapi import Form, File
from pydantic import BaseModel, Field, field_validator

from app.constants.model import GoogleNanoBananaModels

class ImageToImageRequestBasie(BaseModel):
    model:GoogleNanoBananaModels = Field(
        ...,
        title="Nano Banana 모델명",
        description="사용할 Nano Banana 모델 이름"
    )
    image:bytes = Field(
        ...,
        title="입력 이미지 파일",
        description="이미지 변환에 사용할 입력 이미지 파일",
    )
    # candidateCount:int = Field(
    #     1
    # )
    