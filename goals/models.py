from django.db import models
from django.conf import settings


class Goal(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    GOAL_CHOICES = [
        ("Weight Loss", "Weight Loss"),
        ("Weight Gain", "Weight Gain"),
        ("Muscle Gain", "Muscle Gain"),
        ("Maintain Weight", "Maintain Weight"),
    ]

    goal_type = models.CharField(
        max_length=50,
        choices=GOAL_CHOICES,
        default="Weight Loss"
    )

    target_weight = models.FloatField(
        default=0
    )

    start_date = models.DateField()

    end_date = models.DateField()


    def __str__(self):
        return self.goal_type