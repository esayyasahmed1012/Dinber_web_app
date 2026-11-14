def site_context(request):
    from apps.core.models import SiteSettings
    from apps.pages.models import Page

    return {
        "site_settings": SiteSettings.objects.first(),
        "published_pages": Page.objects.filter(
            status=Page.Status.PUBLISHED
        ).order_by("title"),
    }