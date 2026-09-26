from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone

from goals.models import Goal
from water.models import WaterIntake
from weight.models import StepTracker, WeightTracker
from workout.models import Workout


@login_required
def index(request):
    """Render a summary dashboard from the current user's tracker data."""
    user = request.user
    latest_weight = WeightTracker.objects.filter(user=user).order_by("-date", "-id").first()
    water_total = WaterIntake.objects.filter(user=user).aggregate(total=Sum("amount"))["total"] or 0
    steps_today = StepTracker.objects.filter(
        user=user,
        step_date=timezone.localdate(),
    ).aggregate(total=Sum("steps"))["total"] or 0
    return render(request, "dashboard/indesx.html", {
        "weight": latest_weight.weight if latest_weight else None,
        "water": water_total,
        "workout": Workout.objects.filter(user=user).count(),
        "goal": Goal.objects.filter(user=user).count(),
        "steps_today": steps_today,
    })
