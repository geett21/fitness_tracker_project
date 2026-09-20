from django.contrib import admin
from .models import WeightTracker


@admin.register(WeightTracker)
class WeightAdmin(admin.ModelAdmin):
    list_display = ('user','weight','goal','date')