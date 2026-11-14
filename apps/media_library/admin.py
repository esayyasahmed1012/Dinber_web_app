from django.contrib import admin

from .models import MediaImage, VideoLesson


@admin.register(MediaImage)
class MediaImageAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "status",
        "is_featured",
        "uploaded_by",
        "created_at",
    )

    list_filter = (
        "status",
        "is_featured",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "alt_text",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_per_page = 20
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(VideoLesson)
class VideoLessonAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "status",
        "is_featured",
        "uploaded_by",
        "created_at",
    )

    list_filter = (
        "status",
        "category",
        "is_featured",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "category",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    readonly_fields = (
        "created_at",
        "updated_at",
        "published_at",
    )

    list_per_page = 20
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
