from django.contrib import admin
from django.utils.html import format_html

from config.admin import admin_site
from image.models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image_thumbnail",
        "file_url",
        "file_hash",
        "created_at",
        "modified_at",
    )
    fields = (
        "id",
        "image_thumbnail",
        "file_url",
        "file_hash",
        "created_at",
        "modified_at",
    )
    readonly_fields = (
        "id",
        "image_thumbnail",
        "file_hash",
        "created_at",
        "modified_at",
    )
    list_per_page = 1000

    def image_thumbnail(self, obj):
        return format_html(
            '<img src="{}" alt="Image" style="max-height: 128px; max-width: 128px;" />',  # noqa: E501
            obj.file_url,
        )

    image_thumbnail.short_description = "Thumbnail"


admin_site.register(Image, ImageAdmin)
