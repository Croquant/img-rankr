from django.contrib import admin

from config.admin import admin_site

from .models import Elo, EloHistory, Match


class EloAdmin(admin.ModelAdmin):
    list_display = (
        "image",
        "score",
        "n_games",
        "n_wins",
        "n_losses",
        "created_at",
        "modified_at",
    )
    list_filter = ("created_at", "modified_at")
    readonly_fields = ("created_at", "modified_at")


class EloHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "elo", "previous_score", "new_score", "timestamp")
    list_filter = ("timestamp",)
    readonly_fields = ("id", "timestamp")


class MatchAdmin(admin.ModelAdmin):
    pass


admin_site.register(Elo, EloAdmin)
admin_site.register(EloHistory, EloHistoryAdmin)
admin_site.register(Match, MatchAdmin)
