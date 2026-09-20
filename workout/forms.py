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
        ("Squats", "Squats"),
        ("Plank", "Plank"),
        ("Jumping Jacks", "Jumping Jacks"),
        ("Burpees", "Burpees"),
        ("HIIT", "HIIT"),
        ("Weight Training", "Weight Training"),
        ("Full Body Workout", "Full Body Workout"),
    ]

    name = forms.ChoiceField(
        choices=WORKOUT_OPTIONS,
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
            "category",
            "duration",
            "calories_burned",
        ]

        widgets = {

            "name": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "duration": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Duration (Minutes)"
                }
            ),

            "calories_burned": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Calories Burned"
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
                    "placeholder": "Duration Minutes"
                }
            ),

            "calories": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Calories"
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
                    "placeholder": "Duration Minutes"
                }
            ),

            "benefits": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Benefits"
                }
            ),
        }
