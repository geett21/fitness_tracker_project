from django.db import models
from django.conf import settings


# ==========================
# Nutrition Tip
# ==========================
class NutritionTip(models.Model):

    title = models.CharField(max_length=100)

    description = models.TextField()

    def __str__(self):
        return self.title


# ==========================
# Food Diary
# ==========================
class FoodDiary(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    MEAL_CHOICES = (
        ("Breakfast", "Breakfast"),
        ("Lunch", "Lunch"),
        ("Dinner", "Dinner"),
        ("Snack", "Snack"),
    )

    meal = models.CharField(
        max_length=20,
        choices=MEAL_CHOICES
    )

    food_name = models.CharField(max_length=100)

    calories = models.PositiveIntegerField()

    protein = models.FloatField(default=0)

    carbs = models.FloatField(default=0)

    fats = models.FloatField(default=0)

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_name} ({self.meal})"


# ==========================
# Meal Plan
# ==========================
class MealPlan(models.Model):

    GOAL_CHOICES = (
        ("Weight Loss", "Weight Loss"),
        ("Weight Gain", "Weight Gain"),
        ("Maintain", "Maintain"),
    )

    goal = models.CharField(
        max_length=20,
        choices=GOAL_CHOICES
    )

    breakfast = models.TextField()

    lunch = models.TextField()

    dinner = models.TextField()

    snacks = models.TextField(blank=True)

    def __str__(self):
        return self.goal