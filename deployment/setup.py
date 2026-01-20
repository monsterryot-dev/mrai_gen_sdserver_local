# TODO: setup 정리 필요
import os
import subprocess
from cx_Freeze import setup, Executable

def detect_cuda_version():
    """CUDA 버전 자동 감지"""
    try:
        result = subprocess.run(
            ["nvcc", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        if "release 11" in result.stdout:
            return "cuda11"
        elif "release 12" in result.stdout:
            return "cuda12"
    except:
        pass
    return "cpu"

# 환경변수 또는 자동 감지
cuda_mode = os.environ.get("CUDA_VERSION", detect_cuda_version())
print(f"빌드 모드: {cuda_mode}")

# 기본 패키지
common_packages = [
    "os", "sys", "fastapi", "uvicorn", "starlette", 
    "anyio", "pydantic", "typing_extensions",
]

# 서비스 관련 패키지
service_packages = [
    "win32service", "win32serviceutil", "win32event", 
    "servicemanager",
]

# CUDA 버전별 패키지
if cuda_mode in ["cuda11", "cuda12"]:
    gpu_packages = ["torch", "torchvision", "pynvml"]
    common_packages += gpu_packages + service_packages
else:
    # CPU 모드
    cpu_packages = ["torch", "torchvision"]
    common_packages += cpu_packages + service_packages

build_exe_options = {
    "packages": common_packages,
    "includes": [
        "win32timezone",
        "uvicorn.logging",
        "uvicorn.loops.auto",
        "uvicorn.protocols.http.auto",
        "uvicorn.protocols.websockets.auto",
        "uvicorn.lifespan.on",
    ],
    "include_files": [
        # 필요한 파일 추가
        # ("server.json", "server.json"),
    ],
    "excludes": [
        "tkinter", "unittest", "email", "http.server",
        "matplotlib", "PIL", "numpy.distutils",
    ],
    "optimize": 2,
}

# MSI 옵션
bdist_msi_options = {
    "upgrade_code": "{12345678-1234-1234-1234-123456789012}",
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\MRAI_SDServer",
}

executable = Executable(
    script="start.py",
    base=None,
    target_name=f"MRAI_Server_{cuda_mode}.exe",
)

setup(
    name="MRAI_SDServer",
    version="1.2.0",
    description=f"MRAI AI Local Server ({cuda_mode})",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=[executable]
)
