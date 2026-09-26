from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import WeightTracker
from .forms import WeightForm


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


@login_required
def bmi_calculator(request):
    bmi = None
    status = None
    error = None

    if request.method == "POST":
        try:
            weight = float(request.POST.get("weight", ""))
            height = float(request.POST.get("height", "")) / 100

            if weight <= 0 or height <= 0:
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