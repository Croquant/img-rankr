from ninja import NinjaAPI

from elo.api import router as elo_router
from image.api import router as image_router

api = NinjaAPI()


@api.get("/ping")
def hello(request):
    return "pong"


# ROUTERS
api.add_router("/image/", image_router)
api.add_router("/elo/", elo_router)
