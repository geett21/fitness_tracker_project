import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render


COACH_INSTRUCTIONS = (
    "You are FitTrack's supportive fitness coach. Answer questions about general "
    "exercise, nutrition, recovery, and healthy habits clearly and concisely. "
    "Do not diagnose conditions or replace medical care. For symptoms, injuries, "
    "pregnancy, eating disorders, or personalised treatment, advise consulting a "
    "qualified healthcare professional."
)


def _response_text(response_data):
    """Extract generated text from a Responses API payload."""
    if response_data.get("output_text"):
        return response_data["output_text"].strip()

    parts = []
    for item in response_data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text" and content.get("text"):
                parts.append(content["text"])
    return "\n".join(parts).strip()


def _fallback_coach_reply(question):
    """Return a useful offline answer when AI credentials are unavailable."""
    question_text = (question or "").strip()
    if not question_text:
        return "Ask a fitness or nutrition question and I will help you build a simple plan."

    lower_question = question_text.lower()

    if lower_question in {"hi", "hello", "hey", "hii", "hey there", "hello there"}:
        return "Hi! I can help with workouts, nutrition, recovery, and healthy habits. What would you like to improve today?"

    if any(word in lower_question for word in ["what should i eat", "eat after", "post workout", "after workout", "after a workout", "after training"]):
        return "After a workout, eat a meal with both protein and carbohydrates. Good options are chicken + rice, yogurt + fruit, paneer + roti, or eggs + oats. Also drink water to rehydrate."

    if any(word in lower_question for word in ["diet", "food", "eat", "meal", "nutrition", "protein", "calorie"]):
        return "For a balanced diet, include protein, vegetables, healthy carbs, and healthy fats in each meal. A simple pattern is: breakfast with protein, lunch with rice or roti + dal/vegetables, dinner with lean protein + salad, and a light snack if needed."

    if any(word in lower_question for word in ["workout", "exercise", "gym", "training", "strength", "cardio"]):
        return "A simple workout plan is 3 to 4 days of training, with 1-2 rest days, proper warm-up, controlled reps, and enough sleep for recovery."

    if any(word in lower_question for word in ["fat", "weight loss", "lose", "reduce", "burn"]):
        return "For weight loss, focus on daily movement, a consistent calorie deficit, high-protein meals, and sleep. You do not need extreme diets; small steady habits work best."

    if any(word in lower_question for word in ["muscle", "gain", "bulk", "build"]):
        return "To build muscle, lift with progressive overload, eat enough protein, and recover well with sleep and rest days. Aim for 1.6-2.2 g of protein per kg of body weight."

    return "Hi! I can help with fitness, nutrition, and healthy routines. Tell me your goal and I’ll give you a simple plan."


def _generate_coach_reply(question):
    """Use OpenAI when configured, while keeping the coach usable offline."""
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
        # Keep the chat available if the key, network, quota, or model is unavailable.
        pass

    return _fallback_coach_reply(question)


def _parse_json_request(request):
    if request.content_type == "application/json":
        try:
            return json.loads(request.body.decode("utf-8") or "{}")
        except Exception:
            return {}
    return request.POST.dict()


def ai_home(request):
    return render(request, 'ai_coach/index.html')


def ai_coach_reply(request):
    """Return a concise response for the coach's quick-question widget."""
    question = request.GET.get("q") or request.POST.get("q") or ""
    if not question.strip():
        reply = "Ask a fitness or nutrition question to get started."
    else:
        reply = "After training, choose a balanced meal with protein, carbohydrates, and water."
    return JsonResponse({"reply": reply, "question": question.strip()})


def diet_suggestion(request):
    return render(request, 'ai_coach/diet_suggestion.html')


def workout_suggestion(request):
    return render(request, 'ai_coach/workout_suggestion.html')


def motivation(request):
    return render(request, 'ai_coach/motivation.html')


def chat_assistant(request):
    if request.method == "POST":
        data = _parse_json_request(request)
        question = (data.get("question") or data.get("message") or "").strip()

        if not question:
            return JsonResponse({"error": "Please enter a question."}, status=400)

        answer = _generate_coach_reply(question)
        return JsonResponse({"response": answer, "question": question})

    return render(request, 'ai_coach/chat_assistant.html', {'answer': '', 'error': ''})


def chat(request):
    return chat_assistant(request)


def bmi_analysis(request):
    if request.method == "POST":
        weight = request.POST.get("weight")
        height = request.POST.get("height")
        try:
            weight = float(weight)
            height = float(height)
            bmi = weight / (height / 100) ** 2 if height > 0 else None
        except (TypeError, ValueError):
            bmi = None
        return render(request, 'ai_coach/bmi.html', {"bmi": bmi})
    return render(request, 'ai_coach/bmi.html')


def api_bmi(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    data = _parse_json_request(request)
    try:
        weight = float(data.get("weight", None))
        height = float(data.get("height", None))
        bmi = weight / (height / 100) ** 2 if height > 0 else None
    except (TypeError, ValueError):
        return JsonResponse({"error": "invalid weight or height"}, status=400)
    category = None
    if bmi is not None:
        if bmi < 18.5:
            category = "underweight"
        elif bmi < 25:
            category = "normal"
        elif bmi < 30:
            category = "overweight"
        else:
            category = "obese"
    return JsonResponse({"bmi": bmi, "category": category})


def api_workout(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    data = _parse_json_request(request)
    goal = (data.get("goal") or "general").lower()
    level = (data.get("level") or "beginner").lower()
    suggestions = []
    if goal == "strength":
        suggestions = ["3x/week full-body resistance training", "Progressive overload"]
    elif goal == "endurance":
        suggestions = ["4x/week steady-state cardio", "One long run per week"]
    else:
        suggestions = ["Mix of cardio and resistance 3x/week", "2 active recovery days"]
    if level == "beginner":
        suggestions = [s + " (lower intensity)" for s in suggestions]
    return JsonResponse({"goal": goal, "level": level, "suggestions": suggestions})


def api_diet(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    data = _parse_json_request(request)
    calories = data.get("calories")
    preference = data.get("preference", "balanced")
    try:
        calories = int(calories) if calories is not None else None
    except (TypeError, ValueError):
        return JsonResponse({"error": "invalid calories"}, status=400)
    plan = {
        "breakfast": "Oatmeal with fruit",
        "lunch": "Grilled chicken salad",
        "dinner": "Baked fish with vegetables",
    }
    if preference == "vegetarian":
        plan = {"breakfast": "Greek yogurt and fruit", "lunch": "Quinoa salad", "dinner": "Tofu stir-fry"}
    return JsonResponse({"calories": calories, "preference": preference, "plan": plan})


def api_chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    data = _parse_json_request(request)
    question = (data.get("question") or data.get("message") or "").strip()
    if not question:
        return JsonResponse({"error": "question is required"}, status=400)
    response = _generate_coach_reply(question)
    return JsonResponse({"question": question, "response": response})