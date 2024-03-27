from ninja import NinjaAPI

from image.api import router as image_router

api = NinjaAPI()


@api.get("/ping")
def hello(request):
    return "pong"


# ROUTERS
api.add_router("/image/", image_router)
