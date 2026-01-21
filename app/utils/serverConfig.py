import os
import json

from app.core.decorators.file import fileContext

def getServerInfo():
    with fileContext("server.json", "r") as f:
        config = json.load(f)
    return config