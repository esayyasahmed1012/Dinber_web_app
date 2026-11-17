from django.shortcuts import render, get_object_or_404
from .models import Announcement


def announcement_list(request):

    announcements = Announcement.objects.filter(
        status=Announcement.Status.PUBLISHED
    ).order_by("-published_at")

    return render(
        request,
        "public/announcement_list.html",
        {
            "announcements": announcements,
        }
    )


def announcement_detail(request, slug):

    announcement = get_object_or_404(
        Announcement,
        slug=slug,
        status=Announcement.Status.PUBLISHED
    )

    return render(
        request,
        "public/announcement_detail.html",
        {
            "announcement": announcement,
        }
    )