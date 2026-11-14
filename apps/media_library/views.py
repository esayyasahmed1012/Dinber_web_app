from urllib.parse import urlparse, parse_qs

from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import MediaImage, VideoLesson


def image_gallery(request):
    images = MediaImage.objects.filter(
        status=MediaImage.Status.PUBLISHED
    ).order_by("-created_at")

    return render(
        request,
        "public/gallery.html",
        {"images": images},
    )


def get_video_embed_url(video_url):
    """
    Convert ordinary YouTube and Vimeo URLs
    into safe, supported embed URLs.
    """

    if not video_url:
        return None

    parsed = urlparse(video_url)
    host = (parsed.hostname or "").lower()
    path_parts = [part for part in parsed.path.split("/") if part]

    # YouTube
    if host in ("youtube.com", "www.youtube.com", "m.youtube.com"):
        video_id = parse_qs(parsed.query).get("v", [None])[0]

        if not video_id and len(path_parts) >= 2:
            if path_parts[0] in ("embed", "shorts"):
                video_id = path_parts[1]

        if video_id:
            return f"https://www.youtube-nocookie.com/embed/{video_id}"

    # Short YouTube URLs
    if host == "youtu.be" and path_parts:
        return f"https://www.youtube-nocookie.com/embed/{path_parts[0]}"

    # Vimeo
    if host in ("vimeo.com", "www.vimeo.com"):
        if path_parts and path_parts[0].isdigit():
            return f"https://player.vimeo.com/video/{path_parts[0]}"

    return None


def video_library(request):
    lessons = VideoLesson.objects.filter(
        status=VideoLesson.Status.PUBLISHED
    )

    search_query = request.GET.get("q", "").strip()

    if search_query:
        lessons = lessons.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(category__icontains=search_query)
        )

    return render(
        request,
        "public/video_library.html",
        {
            "lessons": lessons,
            "search_query": search_query,
        },
    )


def video_detail(request, slug):
    lesson = get_object_or_404(
        VideoLesson,
        slug=slug,
        status=VideoLesson.Status.PUBLISHED,
    )

    embed_url = get_video_embed_url(lesson.video_url)

    return render(
        request,
        "public/video_detail.html",
        {
            "lesson": lesson,
            "embed_url": embed_url,
        },
    )
