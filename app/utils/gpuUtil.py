import pynvml
from contextlib import contextmanager

@contextmanager
def nvmlContext():
    pynvml.nvmlInit()
    try:
        yield
    except Exception as e:
        print(f"NVML Error: {e}")
    finally:
        pynvml.nvmlShutdown()

def getGpuStatus():
    gpuList = []
    with nvmlContext():
        gpuCount = pynvml.nvmlDeviceGetCount()

        for i in range(gpuCount):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle)

            memInfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
            utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
            temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU) 

            gpuInfo = {
                "index": i,
                "name": name,
                "total_memory": memInfo.total // (1024 ** 2),  # in MB
                "used_memory": memInfo.used // (1024 ** 2),    # in MB
                "free_memory": memInfo.free // (1024 ** 2),    # in MB
                "gpu_utilization": utilization.gpu,             # in %
                "memory_utilization": utilization.memory,        # in %
                "temperature": temp                              # in Celsius
            }
            gpuList.append(gpuInfo)

    return gpuList

def getGpuCount():
    with nvmlContext():
        return pynvml.nvmlDeviceGetCount()