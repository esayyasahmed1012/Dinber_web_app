from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300, blank=True)

    logo = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True
    )

    contact_email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=300, blank=True)

    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    footer_text = models.TextField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.site_name