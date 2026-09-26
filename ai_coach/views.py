import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render


COACH_INSTRUCTIONS = (
    "You are FitTrack's supportive fitness coach. Answer questions about "
    "general exercise, nutrition, recovery, hydration, sleep, and healthy "
    "habits clearly and concisely. Give general educational information. "
    "Do not diagnose medical conditions or replace professional medical care. "
    "For symptoms, injuries, illness, pregnancy, eating disorders, or "
    "personalised medical treatment, advise consulting a qualified healthcare "
    "professional."
)


def _response_text(response_data):
    """Extract generated text from a Responses API payload."""
    if response_data.get("output_text"):
        return response_data["output_text"].strip()

    parts = []

    for item in response_data.get("output", []):
        for content in item.get("content", []):
            if (
                content.get("type") == "output_text"
                and content.get("text")
            ):
                parts.append(content["text"])

    return "\n".join(parts).strip()


def _fallback_coach_reply(question):
    """Useful offline answer when AI credentials are unavailable."""

    question_text = (question or "").strip()

    if not question_text:
        return (
            "Ask a fitness, nutrition, recovery, hydration, or healthy "
            "habit question and I will help."
        )

    lower_question = question_text.lower()

    if lower_question in {
        "hi",
        "hello",
        "hey",
        "hii",
        "hey there",
        "hello there",
    }:
        return (
            "Hi! I can help with workouts, nutrition, recovery, hydration, "
            "sleep, and healthy habits. What would you like to know?"
        )

    if any(
        word in lower_question
        for word in [
            "after workout",
            "post workout",
            "after training",
            "after exercise",
        ]
    ):
        return (
            "After exercise, have a balanced meal or snack containing "
            "protein and carbohydrates, and drink enough water. Examples "
            "include yogurt with fruit, paneer with roti, or eggs with oats."
        )

    if any(
        word in lower_question
        for word in [
            "diet",
            "food",
            "eat",
            "meal",
            "nutrition",
            "protein",
        ]
    ):
        return (
            "For balanced nutrition, include a variety of vegetables, "
            "fruits, whole grains, protein foods, and healthy fats. Regular "
            "meals, enough fluids, and variety are more useful than extreme "
            "diet rules."
        )

    if any(
        word in lower_question
        for word in [
            "workout",
            "exercise",
            "gym",
            "training",
            "strength",
            "cardio",
        ]
    ):
        return (
            "A balanced fitness routine can include aerobic activity, "
            "strength exercises, mobility work, rest, and good sleep. "
            "Start at a comfortable level and increase activity gradually."
        )

    if any(
        word in lower_question
        for word in [
            "sleep",
            "recovery",
            "rest",
        ]
    ):
        return (
            "Recovery is an important part of fitness. Prioritize regular "
            "sleep, rest between demanding sessions, hydration, and balanced "
            "meals."
        )

    if any(
        word in lower_question
        for word in [
            "water",
            "hydration",
            "drink",
        ]
    ):
        return (
            "Drink water regularly throughout the day and pay attention to "
            "thirst, activity, and hot weather. During longer or harder "
            "exercise, hydration needs can be higher."
        )

    if any(
        word in lower_question
        for word in [
            "pain",
            "injury",
            "dizzy",
            "hurt",
            "sick",
        ]
    ):
        return (
            "If you have pain, dizziness, an injury, or other concerning "
            "symptoms, stop the activity and speak with a qualified "
            "healthcare professional."
        )

    return (
        "I can help with fitness, nutrition, hydration, recovery, sleep, "
        "and healthy routines. Tell me what you want to know."
    )


def _generate_coach_reply(question):
    """Use OpenAI when configured, otherwise use the offline coach."""

    if not settings.OPENAI_API_KEY:
        return _fallback_coach_reply(question)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            instructions=COACH_INSTRUCTIONS,
            input=question,
            max_output_tokens=300,
        )

        answer = getattr(response, "output_text", "") or ""

        if answer.strip():
            return answer.strip()

    except Exception:
        pass

    return _fallback_coach_reply(question)


def _parse_json_request(request):
    if request.content_type == "application/json":
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
            return payload if isinstance(payload, dict) else {}
        except Exception:
            return {}

    return request.POST.dict()


# ==========================
# AI COACH HOME
# ==========================

@login_required
def ai_home(request):
    return render(request, "ai_coach/index.html")


# ==========================
# QUICK REPLY
# ==========================

@login_required
def ai_coach_reply(request):

    question = (
        request.GET.get("q")
        or request.POST.get("q")
        or ""
    )

    if not question.strip():
        reply = (
            "Ask a fitness or nutrition question to get started."
        )
    else:
        reply = _generate_coach_reply(question)

    return JsonResponse({
        "reply": reply,
        "question": question.strip(),
    })


# ==========================
# DIET SUGGESTION
# ==========================

@login_required
def diet_suggestion(request):
    return render(
        request,
        "ai_coach/diet_suggestion.html"
    )


# ==========================
# WORKOUT SUGGESTION
# ==========================

@login_required
def workout_suggestion(request):
    return render(
        request,
        "ai_coach/workout_suggestion.html"
    )


# ==========================
# MOTIVATION
# ==========================

@login_required
def motivation(request):
    return render(
        request,
        "ai_coach/motivation.html"
    )


# ==========================
# CHAT ASSISTANT
# ==========================

@login_required
def chat_assistant(request):

    if request.method == "POST":

        data = _parse_json_request(request)

        question = (
            data.get("question")
            or data.get("message")
            or ""
        ).strip()

        if not question:
            return JsonResponse(
                {"error": "Please enter a question."},
                status=400,
            )

        answer = _generate_coach_reply(question)

        return JsonResponse({
            "response": answer,
            "question": question,
        })

    return render(
        request,
        "ai_coach/chat_assistant.html",
        {
            "answer": "",
            "error": "",
        },
    )


@login_required
def chat(request):
    return chat_assistant(request)


# ==========================
# BMI
# ==========================

@login_required
def bmi_analysis(request):

    if request.method == "POST":

        weight = request.POST.get("weight")
        height = request.POST.get("height")

        try:
            weight = float(weight)
            height = float(height)

            if weight <= 0 or height <= 0:
                raise ValueError

            bmi = weight / (height / 100) ** 2

        except (TypeError, ValueError):
            bmi = None

        return render(
            request,
            "ai_coach/bmi.html",
            {"bmi": bmi},
        )

    return render(
        request,
        "ai_coach/bmi.html"
    )


# ==========================
# BMI API
# ==========================

@login_required
def api_bmi(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "POST required"},
            status=405,
        )

    data = _parse_json_request(request)

    try:
        weight = float(data.get("weight"))
        height = float(data.get("height"))

        if weight <= 0 or height <= 0:
            raise ValueError

        bmi = weight / (height / 100) ** 2

    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Invalid weight or height"},
            status=400,
        )

    return JsonResponse({
        "bmi": round(bmi, 2),
    })


# ==========================
# WORKOUT API
# ==========================

@login_required
def api_workout(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "POST required"},
            status=405,
        )

    data = _parse_json_request(request)

    goal = (
        data.get("goal")
        or "general"
    ).lower()

    level = (
        data.get("level")
        or "beginner"
    ).lower()

    if goal == "strength":

        suggestions = [
            "Full-body strength exercises",
            "Start with controlled movements",
            "Allow recovery between sessions",
        ]

    elif goal == "endurance":

        suggestions = [
            "Comfortable-paced aerobic activity",
            "Gradually increase duration",
            "Include recovery days",
        ]

    else:

        suggestions = [
            "Mix aerobic and strength activities",
            "Include mobility work",
            "Keep regular recovery days",
        ]

    if level == "beginner":
        suggestions = [
            item + " at a comfortable intensity"
            for item in suggestions
        ]

    return JsonResponse({
        "goal": goal,
        "level": level,
        "suggestions": suggestions,
    })


# ==========================
# DIET API
# ==========================

@login_required
def api_diet(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "POST required"},
            status=405,
        )

    data = _parse_json_request(request)

    preference = (
        data.get("preference")
        or "balanced"
    ).lower()

    plan = {
        "breakfast": "Oats with fruit and yogurt",
        "lunch": "Rice or roti with dal and vegetables",
        "dinner": "Paneer/tofu with roti and vegetables",
    }

    if preference == "vegetarian":

        plan = {
            "breakfast": "Oats with fruit and yogurt",
            "lunch": "Dal, rice or roti, and vegetables",
            "dinner": "Paneer or tofu with roti and vegetables",
        }

    return JsonResponse({
        "preference": preference,
        "plan": plan,
    })


# ==========================
# CHAT API
# ==========================

@login_required
def api_chat(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "POST required"},
            status=405,
        )

    data = _parse_json_request(request)

    question = (
        data.get("question")
        or data.get("message")
        or ""
    ).strip()

    if not question:
        return JsonResponse(
            {"error": "Question is required"},
            status=400,
        )

    response = _generate_coach_reply(question)

    return JsonResponse({
        "question": question,
        "response": response,
    })
