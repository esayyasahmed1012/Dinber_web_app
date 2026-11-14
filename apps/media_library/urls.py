from django.urls import path

from . import views

app_name = "media_library"

urlpatterns = [
    path("gallery/", views.image_gallery, name="gallery"),

    path("learning-centre/", views.video_library, name="video_library"),

    path(
        "learning-centre/<slug:slug>/",
        views.video_detail,
        name="video_detail",
    ),
]
