from fastapi import FastAPI

from app.constants.router import routerJson

from app.utils.validators import validateRouter

def loadRouters(app: FastAPI) -> None:
    try:
        for routerItem in routerJson:
            validateRouter(routerItem)
            app.include_router(
                routerItem["router"],
                prefix=routerItem["prefix"],
                tags=routerItem.get("tags", None),
            )
    except ValueError:
        pass
    except Exception as e:
        print(f"Error loading routers: \n {e}")