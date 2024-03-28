import os

from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path


class CustomAdminSite(admin.AdminSite):

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("env/", self.environment_view, name="env"),
        ]
        return my_urls + urls

    def get_app_list(self, request, **kwargs):
        """Show some links in the admin UI.

        See also https://stackoverflow.com/a/56476261"""
        app_list = super().get_app_list(request, kwargs)
        app_list += [
            {"name": "environment", "app_label": "env_label", "app_url": "env"}
        ]
        return app_list

    def environment_view(self, request):
        # Retrieve environment variables from os.environ
        environment_variables = dict(os.environ)

        env_vars = [
            (key, value) for key, value in environment_variables.items()
        ]

        context = dict(
            self.each_context(request),
            env_vars=env_vars,
        )
        return TemplateResponse(request, "admin_env.html", context)


admin_site = CustomAdminSite(name="myadmin")
admin_site.site_title = "Img Rankr"
admin_site.site_header = "Img Rankr Admin Panel"
admin_site.index_title = "Admin Panel"
