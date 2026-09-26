from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_GET

from .forms import WaterIntakeForm, WaterReminderSettingsForm
from .models import WaterIntake, WaterReminderSettings


@login_required
def water_list(request):
    water = WaterIntake.objects.filter(user=request.user).order_by("-date")
    today = timezone.localdate()
    reminder_settings, _ = WaterReminderSettings.objects.get_or_create(user=request.user)
    today_total = WaterIntake.objects.filter(user=request.user, date=today).aggregate(
        total=Sum("amount")
    )["total"] or 0
    return render(request, "water/water_list.html", {
        "water": water,
        "today_total": today_total,
        "daily_target": reminder_settings.daily_target_liters,
        "water_remaining": max(float(reminder_settings.daily_target_liters) - float(today_total), 0),
        "reminders_enabled": reminder_settings.enabled,
    })


@login_required
def water_reminder_settings(request):
    settings_obj, _ = WaterReminderSettings.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = WaterReminderSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Your water goal and reminder schedule were saved.")
            return redirect("water_reminder")
    else:
        form = WaterReminderSettingsForm(instance=settings_obj)
    return render(request, "water/water_reminder_settings.html", {
        "form": form,
        "reminders_enabled": settings_obj.enabled,
    })


@login_required
@require_GET
def water_reminder_status(request):
    settings_obj = WaterReminderSettings.objects.filter(user=request.user).first()
    if settings_obj is None:
        settings_obj = WaterReminderSettings(user=request.user)

    requested_date = parse_date(request.GET.get("date", ""))
    today = requested_date or timezone.localdate()
    total = WaterIntake.objects.filter(user=request.user, date=today).aggregate(
        total=Sum("amount")
    )["total"] or 0
    target = float(settings_obj.daily_target_liters)
    return JsonResponse({
        "enabled": settings_obj.enabled,
        "daily_target": target,
        "today_total": float(total),
        "remaining": max(target - float(total), 0),
        "interval_minutes": settings_obj.interval_minutes,
        "start_time": settings_obj.start_time.strftime("%H:%M"),
        "end_time": settings_obj.end_time.strftime("%H:%M"),
    })


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

    return render(request, "water/water_form.html", {"form": form})


@login_required
def water_update(request, pk):
    water = get_object_or_404(WaterIntake, pk=pk, user=request.user)

    if request.method == "POST":
        form = WaterIntakeForm(request.POST, instance=water)
        if form.is_valid():
            form.save()
            return redirect("water_list")
    else:
        form = WaterIntakeForm(instance=water)

    return render(request, "water/water_form.html", {"form": form})


@login_required
def water_delete(request, pk):
    water = get_object_or_404(WaterIntake, pk=pk, user=request.user)

    if request.method == "POST":
        water.delete()
        return redirect("water_list")

    return render(request, "water/water_confirm_delete.html", {"water": water})
