import json

def getServerInfo():
    with open("server.json", "r") as f:
        config = json.load(f)
    return config