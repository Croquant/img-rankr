from django.urls import include, path

from .admin import admin_site
from .api import api

urlpatterns = [
    path("", include("frontend.urls")),
    path("admin/", admin_site.urls),
    path("api/", api.urls),
]
