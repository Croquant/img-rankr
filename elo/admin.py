from django.contrib import admin

from .models import Elo, EloHistory


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


admin.site.register(Elo, EloAdmin)
admin.site.register(EloHistory, EloHistoryAdmin)
