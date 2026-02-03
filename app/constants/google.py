from typing import Literal

# imagen
IMAGESIZE = Literal["1k", "2k"]
OUTPUTMIMETYPE = Literal["image/png", "image/jpeg"]
ASPECTRATIO = Literal["1:1", "3:4", "4:3", "9:16", "16:9"]
PERSONGENERATION = Literal["dont_allow", "allow_adult", "allow_all"]

# nano banana
CONTENTIMAGESIZE = Literal["1k", "2k", "4k"]