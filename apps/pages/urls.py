from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),

    path(
        "pages/<slug:slug>/",
        views.page_detail,
        name="page_detail"
    ),
]