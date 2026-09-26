from django.urls import path
from . import views

urlpatterns = [
    path("", views.water_list, name="water_list"),
    path("reminder/", views.water_reminder_settings, name="water_reminder"),
    path("reminder/status/", views.water_reminder_status, name="water_reminder_status"),
    path("add/", views.water_create, name="water_create"),
    path("edit/<int:pk>/", views.water_update, name="water_update"),
    path("delete/<int:pk>/", views.water_delete, name="water_delete"),
]
