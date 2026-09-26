from django.urls import path
from . import views


app_name = "ai_coach"


urlpatterns = [

    path(
        "",
        views.ai_home,
        name="home",
    ),

    path(
        "reply/",
        views.ai_coach_reply,
        name="reply",
    ),

    path(
        "workout/",
        views.workout_suggestion,
        name="ai_workout",
    ),

    path(
        "diet/",
        views.diet_suggestion,
        name="ai_diet",
    ),

    path(
        "bmi/",
        views.bmi_analysis,
        name="bmi",
    ),

    path(
        "motivation/",
        views.motivation,
        name="ai_motivation",
    ),

    path(
        "chat/",
        views.chat_assistant,
        name="chat",
    ),

    # API endpoints

    path(
        "api/bmi/",
        views.api_bmi,
        name="api_bmi",
    ),

    path(
        "api/workout/",
        views.api_workout,
        name="api_workout",
    ),

    path(
        "api/diet/",
        views.api_diet,
        name="api_diet",
    ),

    path(
        "api/chat/",
        views.api_chat,
        name="api_chat",
    ),
]