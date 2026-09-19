from django.urls import path
from . import views

urlpatterns = [
    path("", views.weight_list, name="weight_list"),
    path("add/", views.weight_create, name="weight_create"),
    path("edit/<int:pk>/", views.weight_update, name="weight_update"),
    path("delete/<int:pk>/", views.weight_delete, name="weight_delete"),
    path(
    "bmi/",
    views.bmi_calculator,
    name="bmi_calculator"
),
]