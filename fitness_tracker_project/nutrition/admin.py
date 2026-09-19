from django.contrib import admin
from .models import NutritionTip, FoodDiary, MealPlan


@admin.register(NutritionTip)
class NutritionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
    )


@admin.register(FoodDiary)
class FoodDiaryAdmin(admin.ModelAdmin):
    list_display = ("food_name", "meal", "calories", "protein", "carbs", "fats", "date")
    list_filter = ("meal", "date")
    search_fields = ("food_name",)


@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ("goal", "breakfast", "lunch", "dinner")
