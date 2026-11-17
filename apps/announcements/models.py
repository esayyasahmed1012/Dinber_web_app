from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Announcement(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=250)

    slug = models.SlugField(
        max_length=270,
        unique=True,
        blank=True
    )

    summary = models.CharField(
        max_length=500,
        help_text="A short introduction to the announcement."
    )

    content = models.TextField()

    featured_image = models.ImageField(
        upload_to="announcements/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    is_featured = models.BooleanField(default=False)

    published_at = models.DateTimeField(
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_announcements"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"