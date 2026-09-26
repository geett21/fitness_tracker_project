from django import forms
from .models import Workout, Exercise, Yoga


# ==========================
# Workout Form
# ==========================

class WorkoutForm(forms.ModelForm):

    WORKOUT_OPTIONS = [
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
    ]

    AGE_OPTIONS = [
        (str(age), str(age))
        for age in range(13, 31)
    ]

    name = forms.ChoiceField(
        choices=WORKOUT_OPTIONS,
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )

    age = forms.ChoiceField(
        choices=AGE_OPTIONS,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = Workout

        fields = [
            "name",
            "age",
            "category",
            "duration",
            "calories_burned",
        ]

        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "duration": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Duration (Minutes)",
                    "min": "1"
                }
            ),

            "calories_burned": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Calories Burned",
                    "min": "0"
                }
            ),
        }


# ==========================
# Exercise Form
# ==========================

class ExerciseForm(forms.ModelForm):

    class Meta:
        model = Exercise

        fields = [
            "name",
            "muscle",
            "duration",
            "calories",
        ]

        widgets = {
            "name": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "muscle": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Muscle Target"
                }
            ),

            "duration": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Duration Minutes",
                    "min": "1"
                }
            ),

            "calories": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Calories",
                    "min": "0"
                }
            ),
        }


# ==========================
# Yoga Form
# ==========================

class YogaForm(forms.ModelForm):

    class Meta:
        model = Yoga

        fields = [
            "name",
            "level",
            "duration",
            "benefits",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Yoga Name"
                }
            ),

            "level": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Beginner / Intermediate / Advanced"
                }
            ),

            "duration": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Duration Minutes",
                    "min": "1"
                }
            ),

            "benefits": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Benefits",
                    "rows": "4"
                }
            ),
        }