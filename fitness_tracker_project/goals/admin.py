from django.contrib import admin
from .models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = (
        "goal_type",
        "target_weight",
        "start_date",
        "end_date",
    )
