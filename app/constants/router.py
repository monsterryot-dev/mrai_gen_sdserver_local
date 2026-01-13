from typing import List, Dict, Any

from app.routers.v1 import v1Router

routerJson: List[Dict[str, Any]] = [
    {
        "router": v1Router,
        "prefix": "/v1",
        "tags": ["v1"],
    }
]