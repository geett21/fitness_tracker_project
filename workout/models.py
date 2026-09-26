from django.db import models
from django.conf import settings
class Workout(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    CATEGORY = (
        ("Cardio", "Cardio"),
        ("Strength", "Strength"),
        ("Yoga", "Yoga"),
        ("Other", "Other"),
    )


    WORKOUT_NAMES = (
        ("Running", "Running"),
        ("Walking", "Walking"),
        ("Cycling", "Cycling"),
        ("Yoga", "Yoga"),
        ("Push Ups", "Push Ups"),
        ("Pull Ups", "Pull Ups"),
        ("Squats", "Squats"),
        ("Lunges", "Lunges"),
        ("Plank", "Plank"),
        ("Jumping Jacks", "Jumping Jacks"),
        ("Burpees", "Burpees"),
        ("Chest Workout", "Chest Workout"),
        ("Back Workout", "Back Workout"),
        ("Leg Workout", "Leg Workout"),
        ("Shoulder Workout", "Shoulder Workout"),
        ("Arm Workout", "Arm Workout"),
        ("Full Body Workout", "Full Body Workout"),
        ("HIIT", "HIIT"),
        ("Cardio", "Cardio"),
        ("Weight Training", "Weight Training"),
        ("Stretching", "Stretching"),
        ("Meditation", "Meditation"),
    )


    name = models.CharField(
        max_length=100,
    )


    category = models.CharField(
        max_length=50,
        choices=CATEGORY
    )


    duration = models.PositiveIntegerField(
        help_text="Minutes"
    )


    calories_burned = models.PositiveIntegerField()


    date = models.DateField(
        auto_now_add=True
    )


    def __str__(self):
        return self.name



class Exercise(models.Model):

    name = models.CharField(
        max_length=100
    )


    muscle = models.CharField(
        max_length=100
    )


    duration = models.PositiveIntegerField()


    calories = models.PositiveIntegerField()


    def __str__(self):
        return self.name



class Yoga(models.Model):

    name = models.CharField(
        max_length=100
    )


    level = models.CharField(
        max_length=50
    )


    duration = models.PositiveIntegerField()


    benefits = models.TextField()


    def __str__(self):
        return self.name
