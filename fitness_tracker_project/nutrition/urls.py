from django.urls import path
from . import views

urlpatterns = [
    path("", views.nutrition_home, name="nutrition_home"),

    path("calorie/", views.calorie_calculator, name="calorie_calculator"),

    path("food-diary/", views.food_diary, name="food_diary"),

    path("meal-plans/", views.meal_plans, name="meal_plans"),

    path("macro-tracker/", views.macro_tracker, name="macro_tracker"),

    path("tips/", views.nutrition_tips, name="nutrition_tips"),
]