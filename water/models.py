from django.db import models
from django.conf import settings
from datetime import time

from django.core.validators import MaxValueValidator, MinValueValidator


class WaterReminderSettings(models.Model):
    REMINDER_INTERVALS = [
        (30, "Every 30 minutes"),
        (60, "Every hour"),
        (120, "Every 2 hours"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="water_reminder_settings",
    )
    daily_target_liters = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=2.00,
        validators=[MinValueValidator(0.25), MaxValueValidator(10.00)],
    )
    interval_minutes = models.PositiveSmallIntegerField(
        choices=REMINDER_INTERVALS,
        default=120,
    )
    start_time = models.TimeField(default=time(8, 0))
    end_time = models.TimeField(default=time(22, 0))
    enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Water reminders for {self.user}"

class WaterIntake(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    amount = models.FloatField(help_text="Water in Liters")

    date = models.DateField()

    notes = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return f"{self.amount} L - {self.date}"
