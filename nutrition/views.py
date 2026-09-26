from datetime import date
from math import isfinite

from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import FoodDiary, NutritionTip
from .forms import FoodDiaryForm


def calorie_calculator(request):
    calories = None
    error = None

    if request.method == "POST":
        try:
            weight = float(request.POST.get("weight", ""))
            height = float(request.POST.get("height", ""))
            age = int(request.POST.get("age", ""))
            activity = float(request.POST.get("activity", ""))

            if (
                not all(isfinite(value) for value in (weight, height, activity))
                or weight <= 0
                or height <= 0
                or age <= 0
                or activity not in (1.2, 1.5, 1.7)
            ):
                raise ValueError

            # Mifflin-St Jeor equation (male baseline; no sex input exists yet).
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
            calories = round(bmr * activity)
        except (TypeError, ValueError):
            error = "Enter valid positive values and choose an activity level."

    return render(request, "nutrition/calorie_calculator.html", {
        "calories": calories,
        "error": error,
    })

@login_required
def food_diary(request):

    if request.method == "POST":
        form = FoodDiaryForm(request.POST)
        if form.is_valid():
            food_entry = form.save(commit=False)
            food_entry.user = request.user
            food_entry.save()
            return redirect("food_diary")
    else:
        form = FoodDiaryForm()

    foods = FoodDiary.objects.filter(user=request.user).order_by("-date", "-id")
    totals = foods.filter(date=date.today()).aggregate(
        total_calories=Sum("calories"),
        total_protein=Sum("protein"),
        total_carbs=Sum("carbs"),
        total_fats=Sum("fats"),
    )
    totals = {key: value or 0 for key, value in totals.items()}

    return render(request, "nutrition/food_diary.html", {
        "form": form,
        "foods": foods,
        **totals,
    })


def meal_plans(request):
    plans = [
        {
            "name": "Balanced Veg Plan",
            "tag": "Vegetarian",
            "color": "#0f766e",
            "meals": [
                {"type": "Breakfast", "items": "Oats 50 g + milk 200 ml + banana 1 small", "icon": "bi-sunrise-fill"},
                {"type": "Mid-morning", "items": "Apple 1 medium + almonds 10", "icon": "bi-brightness-high-fill"},
                {"type": "Lunch", "items": "Brown rice 1 cup cooked + dal 1 cup + salad 1 bowl", "icon": "bi-sun-fill"},
                {"type": "Evening snack", "items": "Roasted chana 30 g + tea 1 cup", "icon": "bi-cup-hot-fill"},
                {"type": "Dinner", "items": "Paneer 100 g + 2 chapatis + vegetables 1 cup", "icon": "bi-moon-stars-fill"},
            ],
        },
        {
            "name": "High-Protein Veg Plan",
            "tag": "Vegetarian",
            "color": "#1864ab",
            "meals": [
                {"type": "Breakfast", "items": "Besan chilla 2 medium + curd 150 g", "icon": "bi-sunrise-fill"},
                {"type": "Mid-morning", "items": "Greek yogurt 150 g + seeds 1 tbsp", "icon": "bi-brightness-high-fill"},
                {"type": "Lunch", "items": "Tofu 150 g + quinoa 1 cup cooked + salad 1 bowl", "icon": "bi-sun-fill"},
                {"type": "Evening snack", "items": "Sprouts chaat 1 bowl, about 150 g", "icon": "bi-cup-hot-fill"},
                {"type": "Dinner", "items": "Soy chunks 50 g dry + 2 chapatis + vegetables 1 cup", "icon": "bi-moon-stars-fill"},
            ],
        },
        {
            "name": "Balanced Non-Veg Plan",
            "tag": "Non-vegetarian",
            "color": "#9a3412",
            "meals": [
                {"type": "Breakfast", "items": "Boiled eggs 2 + whole-wheat toast 2 slices + fruit 1", "icon": "bi-sunrise-fill"},
                {"type": "Mid-morning", "items": "Curd 150 g + walnuts 4 halves", "icon": "bi-brightness-high-fill"},
                {"type": "Lunch", "items": "Grilled chicken 120 g + rice 1 cup cooked + salad 1 bowl", "icon": "bi-sun-fill"},
                {"type": "Evening snack", "items": "Boiled egg 1 + buttermilk 250 ml", "icon": "bi-cup-hot-fill"},
                {"type": "Dinner", "items": "Fish 120 g + 2 chapatis + vegetables 1 cup", "icon": "bi-moon-stars-fill"},
            ],
        },
        {
            "name": "Chicken Muscle Plan",
            "tag": "Non-vegetarian",
            "color": "#7c2d12",
            "meals": [
                {"type": "Breakfast", "items": "Eggs 3 (2 whites + 1 whole) + oats 50 g", "icon": "bi-sunrise-fill"},
                {"type": "Mid-morning", "items": "Milk 250 ml + banana 1 medium", "icon": "bi-brightness-high-fill"},
                {"type": "Lunch", "items": "Chicken breast 150 g + rice 1.5 cups cooked + vegetables 1 cup", "icon": "bi-sun-fill"},
                {"type": "Post-workout", "items": "Whey protein 1 scoop with water 250 ml", "icon": "bi-lightning-charge-fill"},
                {"type": "Dinner", "items": "Chicken 120 g + 2 chapatis + curd 100 g", "icon": "bi-moon-stars-fill"},
            ],
        },
        {
            "name": "Weight Gain Plan",
            "tag": "Veg and Non-Veg options",
            "color": "#7e22ce",
            "meals": [
                {"type": "Breakfast", "items": "Paneer bhurji 100 g OR eggs 3 + 2 parathas medium", "icon": "bi-sunrise-fill"},
                {"type": "Mid-morning", "items": "Banana shake 300 ml + peanut butter 1 tbsp", "icon": "bi-brightness-high-fill"},
                {"type": "Lunch", "items": "Rajma 1 cup OR chicken 150 g + rice 1.5 cups cooked", "icon": "bi-sun-fill"},
                {"type": "Evening snack", "items": "Peanuts 30 g + fruit 1 medium", "icon": "bi-cup-hot-fill"},
                {"type": "Dinner", "items": "Dal 1 cup + paneer 100 g OR fish 150 g + 2 chapatis", "icon": "bi-moon-stars-fill"},
            ],
        },
    ]

    return render(
        request,
        "nutrition/meal_plans.html",
        {
            "plans": plans
        }
    )

def nutrition_tips(request):
    tips = list(NutritionTip.objects.all())
    if not tips:
        tips = [
            {"title": "Build a balanced plate", "description": "Fill half your plate with vegetables, one quarter with protein, and one quarter with whole grains.", "icon": "bi-pie-chart-fill"},
            {"title": "Prioritize protein", "description": "Include a protein source in every meal to support recovery and help you stay full for longer.", "icon": "bi-lightning-charge-fill"},
            {"title": "Hydrate consistently", "description": "Keep water nearby and sip throughout the day. Thirst is often mistaken for hunger.", "icon": "bi-droplet-fill"},
            {"title": "Choose whole foods", "description": "Make fruit, vegetables, legumes, whole grains, and minimally processed foods your everyday staples.", "icon": "bi-basket2-fill"},
            {"title": "Plan ahead", "description": "Prepare simple meals and snacks in advance so healthy choices are always easy to reach.", "icon": "bi-calendar-check-fill"},
            {"title": "Aim for progress", "description": "Small, sustainable changes matter more than perfection. Build habits you can maintain.", "icon": "bi-graph-up-arrow"},
        ]

    return render(
        request,
        "nutrition/nutrition_tips.html",
        {
            "tips": tips
        }
    )
def nutrition_home(request):
    return render(
        request,
        "nutrition/nutrition_home.html"
    )

@login_required
def macro_tracker(request):
    totals = FoodDiary.objects.filter(user=request.user, date=date.today()).aggregate(
        protein=Sum("protein"),
        carbs=Sum("carbs"),
        fats=Sum("fats"),
    )
    return render(request, "nutrition/macro_tracker.html", {
        "protein": totals["protein"] or 0,
        "carbs": totals["carbs"] or 0,
        "fats": totals["fats"] or 0,
    })
