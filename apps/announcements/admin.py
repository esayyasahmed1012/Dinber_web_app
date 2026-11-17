from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "status",
        "is_featured",
        "published_at",
        "created_by",
    )

    list_filter = (
        "status",
        "is_featured",
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
        "published_at",
        "created_by",
    )

    ordering = ("-created_at",)

    def save_model(self, request, obj, form, change):

        if not obj.pk:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)