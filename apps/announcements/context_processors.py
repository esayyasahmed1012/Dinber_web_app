from django.utils import timezone
from .models import Announcement


def announcement_context(request):

    has_new_announcements = Announcement.objects.filter(
        status=Announcement.Status.PUBLISHED,
        published_at__gte=timezone.now() - timezone.timedelta(days=7)
    ).exists()

    return {
        "has_new_announcements": has_new_announcements,
    }