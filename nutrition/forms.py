from django import forms
from .models import FoodDiary, MealPlan, NutritionTip


# ==========================
# Food Diary Form
# ==========================
class FoodDiaryForm(forms.ModelForm):

    class Meta:
        model = FoodDiary

        fields = [
            "meal",
            "food_name",
            "calories",
            "protein",
            "carbs",
            "fats",
        ]

        widgets = {

            "meal": forms.Select(
                attrs={"class": "form-control"}
            ),

            "food_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Food Name",
                }
            ),

            "calories": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Calories",
                }
            ),

            "protein": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Protein (g)",
                }
            ),

            "carbs": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Carbs (g)",
                }
            ),

            "fats": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Fats (g)",
                }
            ),
        }


# ==========================
# Meal Plan Form
# ==========================
class MealPlanForm(forms.ModelForm):

    class Meta:
        model = MealPlan

        fields = [
            "goal",
            "breakfast",
            "lunch",
            "dinner",
            "snacks",
        ]

        widgets = {

            "goal": forms.Select(
                attrs={"class": "form-control"}
            ),

            "breakfast": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "lunch": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "dinner": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "snacks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }


# ==========================
# Nutrition Tip Form
# ==========================
class NutritionTipForm(forms.ModelForm):

    class Meta:
        model = NutritionTip

        fields = [
            "title",
            "description",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Tip Title",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write Nutrition Tip",
                }
            ),
        }