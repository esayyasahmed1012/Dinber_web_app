from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Page(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    # Main page information
    title = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True
    )

    summary = models.CharField(
        max_length=500,
        blank=True
    )

    content = models.TextField()

    # Featured image
    featured_image = models.ImageField(
        upload_to="pages/",
        blank=True,
        null=True
    )

    # Publication information
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    published_at = models.DateTimeField(
        blank=True,
        null=True
    )

    # SEO information
    meta_title = models.CharField(
        max_length=200,
        blank=True
    )

    meta_description = models.CharField(
        max_length=300,
        blank=True
    )

    # Record management
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
        ordering = ["-created_at"]
        verbose_name = "Website Page"
        verbose_name_plural = "Website Pages"