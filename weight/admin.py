from django.contrib import admin
from .models import SleepTracker, StepTracker, WeightTracker


@admin.register(WeightTracker)
class WeightAdmin(admin.ModelAdmin):
    list_display = ('user','weight','goal','date')


@admin.register(StepTracker)
class StepTrackerAdmin(admin.ModelAdmin):
    list_display = ('user', 'steps', 'step_date')
    list_filter = ('step_date',)
    search_fields = ('user__username',)


@admin.register(SleepTracker)
class SleepTrackerAdmin(admin.ModelAdmin):
    list_display = ('user', 'sleep_hours', 'sleep_date')
    list_filter = ('sleep_date',)
    search_fields = ('user__username',)
