from django.db import models

# Create your models here.

from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


def validate_image_size(image):
    max_size = 10 * 1024 * 1024  # 10 MB

    if image.size > max_size:
        raise ValidationError("Image size must not exceed 10 MB.")


def validate_video_size(video):
    max_size = 500 * 1024 * 1024  # 500 MB

    if video.size > max_size:
        raise ValidationError("Video size must not exceed 500 MB.")


class MediaImage(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)

    image = models.ImageField(
        upload_to="media/images/",
        validators=[validate_image_size],
    )

    alt_text = models.CharField(
        max_length=250,
        help_text="Describe the image for accessibility and SEO.",
    )

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    is_featured = models.BooleanField(default=False)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_images",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Media Image"
        verbose_name_plural = "Media Images"


class VideoLesson(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
    )

    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: Education, Training, Community Development.",
    )

    description = models.TextField()

    video_file = models.FileField(
        upload_to="media/videos/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["mp4", "webm", "mov"]
            ),
            validate_video_size,
        ],
    )

    video_url = models.URLField(
        blank=True,
        help_text="Use an external video URL if you are not uploading a file.",
    )

    thumbnail = models.ImageField(
        upload_to="media/thumbnails/",
        blank=True,
        null=True,
        validators=[validate_image_size],
    )

    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    is_featured = models.BooleanField(default=False)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_video_lessons",
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        has_file = bool(self.video_file)
        has_url = bool(self.video_url)

        if has_file == has_url:
            raise ValidationError(
                "Provide exactly one video source: "
                "upload a video file OR enter a video URL."
            )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Video Lesson"
        verbose_name_plural = "Video Lessons"
