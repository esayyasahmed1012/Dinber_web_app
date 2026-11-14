from django.contrib import admin
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "slug",
        "status",
        "published_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "created_at",
        "published_at",
    )

    search_fields = (
        "title",
        "summary",
        "content",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)