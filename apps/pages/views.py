from django.shortcuts import render, get_object_or_404

from .models import Page


def home(request):
    return render(request, "public/home.html")


def page_detail(request, slug):

    page = get_object_or_404(
        Page,
        slug=slug,
        status=Page.Status.PUBLISHED
    )

    return render(
        request,
        "public/page_detail.html",
        {"page": page}
    )