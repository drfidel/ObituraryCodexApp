from django.contrib import admin
from .models import CondolenceMessage, Reaction


@admin.register(CondolenceMessage)
class CondolenceMessageAdmin(admin.ModelAdmin):
    list_display = ("obituary", "user", "is_approved", "created_at")
    list_filter = ("is_approved",)


admin.site.register(Reaction)
