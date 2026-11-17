from django.urls import path
from . import views

app_name = "announcements"

urlpatterns = [
    path(
        "announcements/",
        views.announcement_list,
        name="list"
    ),

    path(
        "announcements/<slug:slug>/",
        views.announcement_detail,
        name="detail"
    ),
]