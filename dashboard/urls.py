from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="legacy_dashboard"),
]
