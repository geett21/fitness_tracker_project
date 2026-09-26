from django.urls import path
from . import views

urlpatterns = [
    # Weight Tracker
    path("", views.weight_list, name="weight_list"),
    path("add/", views.weight_create, name="weight_create"),
    path("edit/<int:pk>/", views.weight_update, name="weight_update"),
    path("delete/<int:pk>/", views.weight_delete, name="weight_delete"),

    # BMI Calculator
    path("bmi/", views.bmi_calculator, name="bmi_calculator"),

    # Step Tracker
    path("steps/", views.step_tracker, name="step_tracker"),

    # Sleep Tracker
    path("sleep/", views.sleep_tracker, name="sleep_tracker"),
]