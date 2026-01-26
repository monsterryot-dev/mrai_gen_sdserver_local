from enum import Enum

class GoogleImagenModels(str, Enum):
    # IMAGEN_V3 = "imagen-3.0-generate-002"
    IMAGEN_V4 = "imagen-4.0-generate-001"
    IMAGEN_V4_ULTRA = "imagen-4.0-ultra-generate-001"
    IMAGEN_V4_FAST = "imagen-4.0-fast-generate-001"

class GoogleNanoBananaModels(str, Enum):
    NANO_BANANA = "gemini-2.5-flash-image"
    NANO_BANANA_PRO = "gemini-3-pro-image-preview"