from django.urls import path
from . import views

urlpatterns = [
    path("", views.goal_list, name="goal_list"),
    path("add/", views.goal_create, name="goal_create"),
    path("edit/<int:pk>/", views.goal_update, name="goal_update"),
    path("delete/<int:pk>/", views.goal_delete, name="goal_delete"),
]