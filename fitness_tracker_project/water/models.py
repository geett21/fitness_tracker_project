from django.db import models
from django.conf import settings

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