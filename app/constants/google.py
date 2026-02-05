from typing import Literal
from enum import Enum

# google 
defaultGooglePrefix = "google_image"
defaultGoogleFormat = "png"

# imagen
imagenTokenCountModel = "models/gemini-2.0-flash"
imagenInputTokenLimit = 480
imagenImageNamePrefix = "generated_imagen"

imagenImageSizeLiteral = Literal["1k", "2k"]
imagenOutputMimeTypeLiteral = Literal["image/png", "image/jpeg"]
imagenAspectRatioLiteral = Literal["1:1", "3:4", "4:3", "9:16", "16:9"]
imagenPersonGenerationLiteral = Literal["dont_allow", "allow_adult", "allow_all"]
    
# nano banana
contentImageNamePrefix = "generated_nano_banana"

contentImageSizeLiteral = Literal["1k", "2k", "4k"]
contentAspectRatioLiteral = Literal["1:1","2:3","3:2","3:4","4:3","4:5","5:4","9:16","16:9","21:9"]
