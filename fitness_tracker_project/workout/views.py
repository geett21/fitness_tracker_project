from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Workout
from .forms import WorkoutForm


# ==========================
# Workout List
# ==========================
@login_required
def workout_list(request):
    workouts = Workout.objects.filter(
        user=request.user
    ).order_by("-date")

    return render(
        request,
        "workout/workout_list.html",
        {"workouts": workouts}
    )


# ==========================
# Add Workout
# ==========================
@login_required
def workout_create(request):
    if request.method == "POST":
        form = WorkoutForm(request.POST)

        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()

            return redirect("workout_list")
    else:
        form = WorkoutForm()

    return render(
        request,
        "workout/workout_form.html",
        {"form": form}
    )


# ==========================
# Update Workout
# ==========================
@login_required
def workout_update(request, pk):
    workout = get_object_or_404(
        Workout,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        form = WorkoutForm(
            request.POST,
            instance=workout
        )

        if form.is_valid():
            form.save()
            return redirect("workout_list")
    else:
        form = WorkoutForm(instance=workout)

    return render(
        request,
        "workout/workout_form.html",
        {"form": form}
    )


# ==========================
# Delete Workout
# ==========================
@login_required
def workout_delete(request, pk):
    workout = get_object_or_404(
        Workout,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        workout.delete()
        return redirect("workout_list")

    return render(
        request,
        "workout/workout_confirm_delete.html",
        {"workout": workout}
    )


# ==========================
# Workout Detail
# ==========================
@login_required
def workout_detail(request, pk):
    workout = get_object_or_404(
        Workout,
        pk=pk,
        user=request.user
    )

    return render(
        request,
        "workout/workout_detail.html",
        {"workout": workout}
    )


# ==========================
# Workout Plans
# ==========================
@login_required
def workout_plans(request):
    return render(
        request,
        "workout/workout_plans.html"
    )


# ==========================
# Daily Workout
# ==========================
@login_required
def daily_workout(request):
    return render(
        request,
        "workout/daily_workout.html"
    )


# ==========================
# Exercise Library
# ==========================
@login_required
def exercise_library(request):
    return render(
        request,
        "workout/excercise_library.html"
    )


# ==========================
# Workout History
# ==========================
@login_required
def workout_history(request):
    workouts = Workout.objects.filter(
        user=request.user
    ).order_by("-date")

    return render(
        request,
        "workout/workout_history.html",
        {"workouts": workouts}
    )


# ==========================
# Yoga
# ==========================
@login_required
def yoga(request):
    return render(
        request,
        "workout/yoga.html"
    )


# ==========================
# Workout Timer
# ==========================
@login_required
def workout_timer(request):
    return render(
        request,
        "workout/workout_timer.html"
    )


# ==========================
# Calories Burned
# ==========================
@login_required
def calories(request):
    workouts = Workout.objects.filter(
        user=request.user
    )

    total = sum(
        workout.calories_burned or 0
        for workout in workouts
    )

    return render(
        request,
        "workout/calories.html",
        {"total_calories": total}
    )