from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum

from weight.models import WeightTracker
from water.models import WaterIntake
from workout.models import Workout


@login_required
def progress_home(request):

    # ==========================
    # Weight Progress
    # ==========================
    weights = WeightTracker.objects.filter(
        user=request.user
    ).order_by("date", "id")

    dates = [
        item.date.strftime("%d %b")
        for item in weights
    ]

    weight_values = [
        item.weight
        for item in weights
    ]

    # ==========================
    # Water Progress
    # ==========================
    water_total = WaterIntake.objects.filter(
        user=request.user
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    # ==========================
    # Workout Progress
    # ==========================
    workout_total = Workout.objects.filter(
        user=request.user
    ).count()

    # ==========================
    # Calories Burned
    # ==========================
    calories_total = Workout.objects.filter(
        user=request.user
    ).aggregate(
        total=Sum("calories_burned")
    )["total"] or 0

    context = {
        "dates": dates,
        "weight_values": weight_values,
        "water_total": water_total,
        "workout_total": workout_total,
        "calories_total": calories_total,
    }

    return render(
        request,
        "progress/progress.html",
        context
    )