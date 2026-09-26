from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone

from goals.models import Goal
from water.models import WaterIntake
from weight.models import StepTracker, WeightTracker
from workout.models import Workout


def base(request):
    return render(request, 'base.html') 
def profile(request):
    return render(request, 'profile.html')  
@login_required
def dashboard(request):
    user = request.user
    latest_weight = WeightTracker.objects.filter(user=user).order_by("-date", "-id").first()
    today_steps = StepTracker.objects.filter(
        user=user,
        step_date=timezone.localdate(),
    ).aggregate(total=Sum("steps"))["total"] or 0
    return render(request, "dashboard.html", {
        "total_goals": Goal.objects.filter(user=user).count(),
        "total_water_entries": WaterIntake.objects.filter(user=user).count(),
        "steps_today": today_steps,
        "latest_weight": latest_weight.weight if latest_weight else None,
        "total_workouts": Workout.objects.filter(user=user).count(),
    })
def goals(request):
    return render(request, 'goals.html')
def water(request):
    return render(request, 'water.html')
def weight(request):
    return render(request, 'weight.html')
def workout(request):
    return render(request, 'workout.html')  

    
