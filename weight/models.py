from django.db import models
from django.conf import settings


class WeightTracker(models.Model):

    GOAL_CHOICES = [
        ('Loss', 'Weight Loss'),
        ('Gain', 'Weight Gain'),
        ('Maintain', 'Maintain Weight'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    weight = models.FloatField(
        help_text="Enter weight in kg"
    )

    height = models.FloatField(
        help_text="Enter height in cm"
    )

    goal = models.CharField(
        max_length=20,
        choices=GOAL_CHOICES,
        default='Maintain'
    )

    date = models.DateField(
        auto_now_add=True
    )


    def bmi(self):
        height_meter = self.height / 100

        if height_meter > 0:
            return round(self.weight / (height_meter ** 2), 2)

        return 0


    def bmi_status(self):
        bmi_value = self.bmi()

        if bmi_value < 18.5:
            return "Underweight"

        elif bmi_value < 25:
            return "Normal"

        elif bmi_value < 30:
            return "Overweight"

        else:
            return "Obese"


    def __str__(self):
        return f"{self.user.username} - {self.weight} kg"
    

class SleepTracker(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sleep_hours = models.FloatField()
    sleep_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.sleep_hours} hours"


class StepTracker(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    steps = models.IntegerField()
    step_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.steps} steps"