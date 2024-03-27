from django.db import models
from ulid import ULID

from .utils import calculate_md5_hash


class Image(models.Model):
    id = models.CharField(
        primary_key=True, max_length=26, default=ULID, editable=False
    )
    file_url = models.URLField(unique=True)
    file_hash = models.CharField(max_length=32, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.file_hash = calculate_md5_hash(self.file_url)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"image({self.id})"
