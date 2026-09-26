from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import WaterIntake
from .forms import WaterIntakeForm


@login_required
def water_list(request):
    water = WaterIntake.objects.filter(
        user=request.user
    ).order_by("-date")

    return render(
        request,
        "water/water_list.html",
        {"water": water}
    )


@login_required
def water_create(request):
    if request.method == "POST":
        form = WaterIntakeForm(request.POST)

        if form.is_valid():
            water_entry = form.save(commit=False)
            water_entry.user = request.user
            water_entry.save()

            return redirect("water_list")
    else:
        form = WaterIntakeForm()

    return render(
        request,
        "water/water_form.html",
        {"form": form}
    )


@login_required
def water_update(request, pk):
    water = get_object_or_404(
        WaterIntake,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        form = WaterIntakeForm(
            request.POST,
            instance=water
        )

        if form.is_valid():
            form.save()
            return redirect("water_list")
    else:
        form = WaterIntakeForm(instance=water)

    return render(
        request,
        "water/water_form.html",
        {"form": form}
    )


@login_required
def water_delete(request, pk):
    water = get_object_or_404(
        WaterIntake,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        water.delete()
        return redirect("water_list")

    return render(
        request,
        "water/water_confirm_delete.html",
        {"water": water}
    )