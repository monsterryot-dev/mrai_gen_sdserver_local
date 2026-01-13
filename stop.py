import requests

from app.utils.serverConfig import getServerInfo

try:
    serverInfo = getServerInfo()
    hostUrl = f"http://{serverInfo['host']}:{serverInfo['port']}/shutdown"
    requests.post(hostUrl, timeout=2)
    print("Server stopped")
except:
    print("Server not running or shutdown failed")