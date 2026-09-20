from django.shortcuts import render, redirect, get_object_or_404
from .models import Workout
from .forms import WorkoutForm


# ==========================
# Workout List
# ==========================
def workout_list(request):
    workouts = Workout.objects.all().order_by("-date")
    return render(
        request,
        "workout/workout_list.html",
        {"workouts": workouts},
    )


# ==========================
# Add Workout
# ==========================
def workout_create(request):
    if request.method == "POST":
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            if request.user.is_authenticated:
                workout.user = request.user
            workout.save()
            return redirect("workout_list")
    else:
        form = WorkoutForm()

    return render(
        request,
        "workout/workout_form.html",
        {"form": form},
    )


# ==========================
# Update Workout
# ==========================
def workout_update(request, pk):
    workout = get_object_or_404(Workout, pk=pk)

    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect("workout_list")
    else:
        form = WorkoutForm(instance=workout)

    return render(
        request,
        "workout/workout_form.html",
        {"form": form},
    )


# ==========================
# Delete Workout
# ==========================
def workout_delete(request, pk):
    workout = get_object_or_404(Workout, pk=pk)

    if request.method == "POST":
        workout.delete()
        return redirect("workout_list")

    return render(
        request,
        "workout/workout_confirm_delete.html",
        {"workout": workout},
    )


# ==========================
# Workout Detail
# ==========================
def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk)

    return render(
        request,
        "workout/workout_detail.html",
        {"workout": workout},
    )


# ==========================
# Workout Plans
# ==========================
def workout_plans(request):
    return render(request, "workout/workout_plans.html")

def daily_workout(request):
    return render(request, "workout/daily_workout.html")


def exercise_library(request):
    return render(request, "workout/excercise_library.html")


def workout_history(request):
    workouts = Workout.objects.all().order_by("-date")
    return render(
        request,
        "workout/workout_history.html",
        {"workouts": workouts},
    )


def yoga(request):
    return render(request, "workout/yoga.html")


def workout_timer(request):
    return render(request, "workout/workout_timer.html")


def calories(request):
    workouts = Workout.objects.all()
    total = sum(w.calories_burned for w in workouts)

    return render(
        request,
        "workout/calories.html",
        {"total_calories": total},
    )
