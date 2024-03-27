from django.contrib import admin
from django.urls import include, path

from frontend import urls

from .api import api

urlpatterns = [
    path("", include("frontend.urls")),
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
