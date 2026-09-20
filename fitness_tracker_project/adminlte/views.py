from django.shortcuts import render

from goals.models import Goal
from water.models import WaterIntake
from weight.models import StepTracker, WeightTracker
from workout.models import Workout


def base(request):
    return render(request, 'base.html') 
def profile(request):
    return render(request, 'profile.html')  
def dashboard(request):
    latest_weight = WeightTracker.objects.order_by("-date", "-id").first()
    return render(request, "dashboard.html", {
        "total_goals": Goal.objects.count(),
        "total_water_entries": WaterIntake.objects.count(),
        "steps_today": StepTracker.objects.order_by("-step_date", "-id").values_list("steps", flat=True).first() or 0,
        "latest_weight": latest_weight.weight if latest_weight else None,
        "total_workouts": Workout.objects.count(),
    })
def goals(request):
    return render(request, 'goals.html')
def water(request):
    return render(request, 'water.html')
def weight(request):
    return render(request, 'weight.html')
def workout(request):
    return render(request, 'workout.html')  

    
