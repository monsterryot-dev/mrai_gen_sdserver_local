from typing import Literal
from enum import Enum

# google 
DEFAULTPREFIX = "google_image"
DEFAULTFORMAT = "png"
DEFAULTSAFEERRORMESSAGE="죄송합니다. 요청하신 콘텐츠는 안전 가이드라인에 따라 생성할 수 없습니다."

# save image type
class SaveImageType(str, Enum):
    IMAGEN = "imagen"
    CONTENT = "content"

# imagen
IMAGENTOKENFINDMODEL = "models/gemini-2.0-flash"
IMAGENINPUTTOKENLIMIT = 480
IMAGENNAMEPREFIX = "generated_imagen"

IMAGESIZE = Literal["1k", "2k"]
OUTPUTMIMETYPE = Literal["image/png", "image/jpeg"]
ASPECTRATIO = Literal["1:1", "3:4", "4:3", "9:16", "16:9"]
PERSONGENERATION = Literal["dont_allow", "allow_adult", "allow_all"]

# nano banana
CONTENTNAMERPREFIX = "generated_nano_banana"
CONTENTIMAGESIZE = Literal["1k", "2k", "4k"]
CONTENTASPECTRATIO = Literal["1:1","2:3","3:2","3:4","4:3","4:5","5:4","9:16","16:9","21:9"]
