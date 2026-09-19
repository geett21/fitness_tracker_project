from django.shortcuts import render

from workout.models import Workout
from water.models import WaterIntake
from weight.models import WeightTracker
from goals.models import Goal


def index(request):

    context = {

        "total_workouts": Workout.objects.filter(user=request.user).count(),

        "total_water": WaterIntake.objects.filter(user=request.user).count(),

        "total_weights": WeightTracker.objects.filter(user=request.user).count(),

        "total_goals": Goal.objects.filter(user=request.user).count(),

    }

    return render(request, "dashboard/index.html", context)