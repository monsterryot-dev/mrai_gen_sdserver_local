# TODO: CX FREEZE를 더 살펴보고 GPU와 관련된 라이브러리 다운로드 적용 시점 설정 예정
from cx_Freeze import setup, Executable

# 상수 설정
SetupName = "Mrai SD Local"
SetupVersion = "1.2.0"
SetupDescription = "MRAI SD Local Application"

buildExeOptions = {
    "include_files": [".env"],
    "excludes": ["tkinter"],
}

setup(
    name=SetupName,
    version=SetupVersion,
    description=SetupDescription,
    options={
        "build_exe": buildExeOptions,
    },
    executables=[]
)