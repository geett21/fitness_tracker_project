from django.urls import path
from . import views

urlpatterns = [
    path("", views.workout_list, name="workout_list"),
    path("plans/", views.workout_plans, name="workout_plans"),
    path("daily/", views.daily_workout, name="daily_workout"),
    path("history/", views.workout_history, name="workout_history"),
    path("exercise/", views.exercise_library, name="exercise_library"),
    path("yoga/", views.yoga, name="yoga"),
    path("timer/", views.workout_timer, name="workout_timer"),
    path("calories/", views.calories, name="calories"),

    path("add/", views.workout_create, name="workout_create"),
    path("edit/<int:pk>/", views.workout_update, name="workout_update"),
    path("delete/<int:pk>/", views.workout_delete, name="workout_delete"),
    path("detail/<int:pk>/", views.workout_detail, name="workout_detail"),
]