from ninja import NinjaAPI

from elo.api import router as elo_router
from image.api import router as image_router

api = NinjaAPI()


@api.get("/hello")
def hello(request):
    return "Hello !"


# ROUTERS
api.add_router("/image/", image_router)
api.add_router("/elo/", elo_router)
