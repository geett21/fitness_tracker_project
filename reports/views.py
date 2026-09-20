from calendar import monthrange
from datetime import date, datetime, timedelta
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from goals.models import Goal
from nutrition.models import FoodDiary
from water.models import WaterIntake
from weight.models import SleepTracker, StepTracker, WeightTracker
from workout.models import Workout


def _parse_week(value):
    try:
        selected = datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        selected = timezone.localdate()
    return selected - timedelta(days=selected.weekday())


def _parse_month(value):
    try:
        selected = datetime.strptime(value, "%Y-%m").date()
    except (TypeError, ValueError):
        selected = timezone.localdate().replace(day=1)
    return selected.replace(day=1)


def _period_details(request, period_type):
    if period_type == "monthly":
        start = _parse_month(request.GET.get("month"))
        end = start.replace(day=monthrange(start.year, start.month)[1])
        label = start.strftime("%B %Y")
        input_value = start.strftime("%Y-%m")
    else:
        start = _parse_week(request.GET.get("week"))
        end = start + timedelta(days=6)
        label = f"{start:%d %b %Y} - {end:%d %b %Y}"
        input_value = start.isoformat()
    return start, end, label, input_value


def _build_report(user, period_type, start, end, label, input_value):
    weights = WeightTracker.objects.filter(
        user=user, date__range=(start, end)
    ).order_by("date", "id")
    steps = StepTracker.objects.filter(
        user=user, step_date__range=(start, end)
    ).order_by("step_date", "id")
    sleep = SleepTracker.objects.filter(
        user=user, sleep_date__range=(start, end)
    ).order_by("sleep_date", "id")
    workouts = Workout.objects.filter(
        user=user, date__range=(start, end)
    ).order_by("date", "id")
    water = WaterIntake.objects.filter(
        user=user, date__range=(start, end)
    ).order_by("date", "id")
    food = FoodDiary.objects.filter(
        user=user, date__range=(start, end)
    ).order_by("date", "id")
    goals = Goal.objects.filter(
        user=user,
        start_date__lte=end,
        end_date__gte=start,
    ).order_by("start_date", "id")

    latest_weight = weights.last()
    total_steps = sum(item.steps for item in steps)
    total_sleep = sum(item.sleep_hours for item in sleep)
    total_water = sum(item.amount for item in water)
    total_calories = sum(item.calories_burned for item in workouts)
    yoga_workouts = workouts.filter(category="Yoga").count()

    metrics = [
        {"label": "Workouts", "value": workouts.count(), "detail": f"{sum(item.duration for item in workouts)} minutes", "icon": "bi-heart-pulse"},
        {"label": "Water intake", "value": f"{total_water:g} L", "detail": f"{water.count()} records", "icon": "bi-droplet"},
        {"label": "Weight records", "value": weights.count(), "detail": f"Latest: {latest_weight.weight:g} kg" if latest_weight else "No records in this period", "icon": "bi-speedometer2"},
        {"label": "Goals / progress", "value": goals.count(), "detail": "Active in this period", "icon": "bi-bullseye"},
        {"label": "Calories burned", "value": f"{total_calories:,}", "detail": f"{workouts.count()} workout records", "icon": "bi-fire"},
        {"label": "Steps", "value": f"{total_steps:,}", "detail": f"{steps.count()} records", "icon": "bi-person-walking"},
        {"label": "Sleep", "value": f"{total_sleep:g} h", "detail": f"{sleep.count()} records", "icon": "bi-moon-stars"},
        {"label": "Yoga workouts", "value": yoga_workouts, "detail": "Included in workout total", "icon": "bi-flower1"},
    ]

    activity_rows = [
        {"date": item.date, "type": "Workout", "value": f"{item.name} - {item.duration} minutes"}
        for item in workouts
    ]
    activity_rows += [
        {"date": item.date, "type": "Water", "value": f"{item.amount:g} L"}
        for item in water
    ]
    activity_rows += [
        {"date": item.date, "type": "Food", "value": f"{item.food_name} - {item.calories} calories"}
        for item in food
    ]
    activity_rows += [
        {"date": item.start_date, "type": "Goal", "value": f"{item.goal_type} - target {item.target_weight:g} kg"}
        for item in goals
    ]
    activity_rows += [
        {"date": item.step_date, "type": "Steps", "value": f"{item.steps:,} steps"}
        for item in steps
    ]
    activity_rows += [
        {"date": item.sleep_date, "type": "Sleep", "value": f"{item.sleep_hours:g} hours"}
        for item in sleep
    ]
    activity_rows += [
        {"date": item.date, "type": "Weight", "value": f"{item.weight:g} kg"}
        for item in weights
    ]
    activity_rows.sort(key=lambda row: row["date"], reverse=True)

    return {
        "period_type": period_type,
        "period_name": "Monthly Report" if period_type == "monthly" else "Weekly Report",
        "period_label": label,
        "input_value": input_value,
        "start": start,
        "end": end,
        "metrics": metrics,
        "activity_rows": activity_rows,
        "data_note": "Reports include records connected to your account for the selected period. Older records created before user ownership was added remain unassigned and are excluded for privacy.",
    }


def _get_report(request, period_type):
    start, end, label, input_value = _period_details(request, period_type)
    return _build_report(request.user, period_type, start, end, label, input_value)


@login_required
def reports_dashboard(request):
    report = _get_report(request, "weekly")
    return render(request, "reports/dashboard.html", {"report": report})


@login_required
def weekly_report(request):
    return render(request, "reports/report.html", {"report": _get_report(request, "weekly")})


@login_required
def monthly_report(request):
    return render(request, "reports/report.html", {"report": _get_report(request, "monthly")})


def _pdf_response(request, period_type):
    report = _get_report(request, period_type)
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=report["period_name"],
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="ReportTitle", parent=styles["Title"], alignment=TA_CENTER, textColor=colors.HexColor("#0d6efd"), spaceAfter=8))
    styles.add(ParagraphStyle(name="Small", parent=styles["Normal"], fontSize=8, textColor=colors.HexColor("#667085")))
    story = [
        Paragraph("Fitness Tracker Report", styles["ReportTitle"]),
        Paragraph(f"<b>User:</b> {request.user.get_full_name() or request.user.username}", styles["Normal"]),
        Paragraph(f"<b>Report:</b> {report['period_name']} | <b>Period:</b> {report['period_label']}", styles["Normal"]),
        Spacer(1, 10),
    ]

    metric_data = [["Metric", "Value", "Details"]] + [
        [metric["label"], str(metric["value"]), metric["detail"]]
        for metric in report["metrics"]
    ]
    metric_table = Table(metric_data, colWidths=[45 * mm, 35 * mm, 90 * mm], repeatRows=1)
    metric_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0d6efd")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#d0d5dd")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f9ff")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [metric_table, Spacer(1, 12), Paragraph("Activity details", styles["Heading2"])]

    activity_data = [["Date", "Activity", "Value"]] + [
        [row["date"].strftime("%d %b %Y"), row["type"], row["value"]]
        for row in report["activity_rows"]
    ]
    if len(activity_data) == 1:
        activity_data.append(["-", "No user-owned records", "-"])
    activity_table = Table(activity_data, colWidths=[45 * mm, 55 * mm, 70 * mm], repeatRows=1)
    activity_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#344054")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#d0d5dd")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9fafb")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [activity_table, Spacer(1, 10), Paragraph(report["data_note"], styles["Small"])]
    document.build(story)
    response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{period_type}-report-{report["start"]}.pdf"'
    return response


@login_required
def weekly_pdf(request):
    return _pdf_response(request, "weekly")


@login_required
def monthly_pdf(request):
    return _pdf_response(request, "monthly")
