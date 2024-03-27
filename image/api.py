from typing import List

from ninja import Router

from .models import Image
from .schemas import (
    AddImageErrorSchema,
    AddImageInputSchema,
    AddImageResponseSchema,
    ImageSchema,
)

router = Router()


@router.post(
    "/add", response={200: AddImageResponseSchema, 400: AddImageErrorSchema}
)
def add_image(request, data: AddImageInputSchema):
    try:
        get_or_create = Image.objects.get_or_create(file_url=data.file_url)
        return {"created": get_or_create[1], "image": get_or_create[0]}
    except Exception as e:
        return 400, {"created": False, "error_message": e.__str__()}


@router.get("/all", response=List[ImageSchema])
def get_all_images(request):
    return Image.objects.all().order_by("-elo__score")
