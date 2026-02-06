"""
이미지 생성 모델 Enum 정의 모듈
"""
from enum import Enum

class GoogleImagenModels(str, Enum):
    IMAGEN_V4 = "imagen-4.0-generate-001"
    IMAGEN_V4_FAST = "imagen-4.0-fast-generate-001"
    IMAGEN_V4_ULTRA = "imagen-4.0-ultra-generate-001"
    IMAGEN_V4_PREVIEW = "imagen-4.0-generate-preview-06-06"
    IMAGEN_V4_PREVIEW_ULTRA = "imagen-4.0-ultra-generate-preview-06-06"

class GoogleGeminiModels(str, Enum):
    NANO_BANANA = "gemini-2.5-flash-image"
    NANO_BANANA_PRO = "gemini-3-pro-image-preview"