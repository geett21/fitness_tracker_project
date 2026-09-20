from django.shortcuts import render

from goals.models import Goal
from water.models import WaterIntake
from weight.models import WeightTracker
from workout.models import Workout


def index(request):
    """Render a summary dashboard from the tracker data."""
    latest_weight = WeightTracker.objects.order_by("-date", "-id").first()
    return render(request, "dashboard/indesx.html", {
        "total_workouts": Workout.objects.count(),
        "total_water_entries": WaterIntake.objects.count(),
        "total_goals": Goal.objects.count(),
        "latest_weight": latest_weight.weight if latest_weight else None,
    })
