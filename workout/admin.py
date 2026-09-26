
from django.contrib import admin

from .models import Workout, Exercise, Yoga


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "category",
        "duration",
        "calories_burned",
        "date",
    )

    list_filter = (
        "category",
        "name",
        "date",
    )

    search_fields = (
        "name",
        "user__username",
        "user__email",
    )


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "muscle",
        "duration",
        "calories",
    )

    list_filter = (
        "muscle",
    )

    search_fields = (
        "name",
        "muscle",
    )


@admin.register(Yoga)
class YogaAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "level",
        "duration",
    )

    list_filter = (
        "level",
    )

    search_fields = (
        "name",
        "level",
    )