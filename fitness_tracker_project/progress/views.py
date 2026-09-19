from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from weight.models import WeightTracker


@login_required
def progress_home(request):
    weights = WeightTracker.objects.filter(user=request.user).order_by("date", "id")

    dates = [item.date.strftime("%d %b") for item in weights]
    weight_values = [item.weight for item in weights]

    context = {
        "dates": dates,
        "weight_values": weight_values,
    }

    return render(request, "progress/progress.html", context)