from django.shortcuts import render, redirect, get_object_or_404
from .models import WaterIntake
from .forms import WaterIntakeForm


def water_list(request):
    water = WaterIntake.objects.all().order_by("-date")
    return render(request, "water/water_list.html", {"water": water})


def water_create(request):
    if request.method == "POST":
        form = WaterIntakeForm(request.POST)
        if form.is_valid():
            water_entry = form.save(commit=False)
            if request.user.is_authenticated:
                water_entry.user = request.user
            water_entry.save()
            return redirect("water_list")
    else:
        form = WaterIntakeForm()

    return render(request, "water/water_form.html", {"form": form})


def water_update(request, pk):
    water = get_object_or_404(WaterIntake, pk=pk)

    if request.method == "POST":
        form = WaterIntakeForm(request.POST, instance=water)
        if form.is_valid():
            form.save()
            return redirect("water_list")
    else:
        form = WaterIntakeForm(instance=water)

    return render(request, "water/water_form.html", {"form": form})


def water_delete(request, pk):
    water = get_object_or_404(WaterIntake, pk=pk)

    if request.method == "POST":
        water.delete()
        return redirect("water_list")

    return render(request, "water/water_confirm_delete.html", {"water": water})