from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from goals.models import Goal
from water.models import WaterIntake
from weight.models import StepTracker, WeightTracker
from workout.models import Workout


def base(request):
    return render(request, "base.html")


@login_required
def profile(request):
    return render(request, "profile.html")


@login_required
def dashboard(request):
    latest_weight = (
        WeightTracker.objects
        .filter(user=request.user)
        .order_by("-date", "-id")
        .first()
    )

    total_goals = Goal.objects.filter(
        user=request.user
    ).count()

    total_water_entries = WaterIntake.objects.filter(
        user=request.user
    ).count()

    steps_today = (
        StepTracker.objects
        .filter(user=request.user)
        .order_by("-step_date", "-id")
        .values_list("steps", flat=True)
        .first()
        or 0
    )

    total_workouts = Workout.objects.filter(
        user=request.user
    ).count()

    return render(request, "dashboard.html", {
        "total_goals": total_goals,
        "total_water_entries": total_water_entries,
        "steps_today": steps_today,
        "latest_weight": latest_weight.weight if latest_weight else None,
        "total_workouts": total_workouts,
    })


def goals(request):
    return render(request, "goals.html")


def water(request):
    return render(request, "water.html")


def weight(request):
    return render(request, "weight.html")


def workout(request):
    return render(request, "workout.html")