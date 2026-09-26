from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from math import isfinite

from .models import WeightTracker, StepTracker, SleepTracker
from .forms import WeightForm


# ==========================
# Weight List
# ==========================
@login_required
def weight_list(request):
    weights = WeightTracker.objects.filter(
        user=request.user
    ).order_by("-date")

    form = WeightForm()

    return render(
        request,
        "weight/weight_list.html",
        {
            "weights": weights,
            "form": form,
        }
    )


# ==========================
# Add Weight
# ==========================
@login_required
def weight_create(request):
    if request.method == "POST":
        form = WeightForm(request.POST)

        if form.is_valid():
            weight = form.save(commit=False)
            weight.user = request.user
            weight.save()

            return redirect("weight_list")
    else:
        form = WeightForm()

    return render(
        request,
        "weight/weight_form.html",
        {"form": form}
    )


# ==========================
# Update Weight
# ==========================
@login_required
def weight_update(request, pk):
    weight = get_object_or_404(
        WeightTracker,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        form = WeightForm(
            request.POST,
            instance=weight
        )

        if form.is_valid():
            form.save()
            return redirect("weight_list")
    else:
        form = WeightForm(instance=weight)

    return render(
        request,
        "weight/weight_form.html",
        {"form": form}
    )


# ==========================
# Delete Weight
# ==========================
@login_required
def weight_delete(request, pk):
    weight = get_object_or_404(
        WeightTracker,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        weight.delete()
        return redirect("weight_list")

    return render(
        request,
        "weight/weight_confirm_delete.html",
        {"weight": weight}
    )


# ==========================
# BMI Calculator
# ==========================
@login_required
def bmi_calculator(request):
    bmi = None
    status = None
    error = None

    if request.method == "POST":
        try:
            weight = float(request.POST.get("weight", ""))
            height = float(request.POST.get("height", "")) / 100

            if not isfinite(weight) or not isfinite(height) or weight <= 0 or height <= 0:
                raise ValueError

            bmi = round(
                weight / (height * height),
                2
            )

            if bmi < 18.5:
                status = "Underweight"
            elif bmi < 25:
                status = "Normal"
            elif bmi < 30:
                status = "Overweight"
            else:
                status = "Obese"

        except (TypeError, ValueError):
            error = "Enter valid positive values for weight and height."

    return render(
        request,
        "weight/bmi_calculator.html",
        {
            "bmi": bmi,
            "status": status,
            "error": error,
        }
    )


# ==========================
# Step Counter
# ==========================
@login_required
def step_tracker(request):

    if request.method == "POST":
        steps = request.POST.get("steps")

        try:
            steps = int(steps)

            if steps < 0:
                raise ValueError

            StepTracker.objects.create(
                user=request.user,
                steps=steps
            )

            return redirect("step_tracker")

        except (TypeError, ValueError):
            error = "Please enter a valid number of steps."
    else:
        error = None

    steps = StepTracker.objects.filter(
        user=request.user
    ).order_by("-step_date", "-id")

    return render(
        request,
        "weight/step_tracker.html",
        {
            "steps": steps,
            "error": error,
        }
    )


# ==========================
# Sleep Tracker
# ==========================
@login_required
def sleep_tracker(request):

    if request.method == "POST":
        sleep_hours = request.POST.get("sleep_hours")

        try:
            sleep_hours = float(sleep_hours)

            if not isfinite(sleep_hours) or sleep_hours < 0:
                raise ValueError

            SleepTracker.objects.create(
                user=request.user,
                sleep_hours=sleep_hours
            )

            return redirect("sleep_tracker")

        except (TypeError, ValueError):
            error = "Please enter valid sleep hours."
    else:
        error = None

    sleep_records = SleepTracker.objects.filter(
        user=request.user
    ).order_by("-sleep_date", "-id")

    return render(
        request,
        "weight/sleep_tracker.html",
        {
            "sleep_records": sleep_records,
            "error": error,
        }
    )
