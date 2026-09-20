from django.shortcuts import render, redirect, get_object_or_404
from .models import Goal
from .forms import GoalForm


def goal_list(request):
    goals = Goal.objects.all()
    return render(request, "goals/goal_list.html", {"goals": goals})


def goal_create(request):
    if request.method == "POST":
        form = GoalForm(request.POST)

        if form.is_valid():
            goal = form.save(commit=False)
            if request.user.is_authenticated:
                goal.user = request.user
            goal.save()
            return redirect("goal_list")
        else:
            print(form.errors)

    else:
        form = GoalForm()

    return render(request, "goals/goal_form.html", {"form": form})


def goal_update(request, pk):
    goal = get_object_or_404(Goal, pk=pk)

    if request.method == "POST":
        form = GoalForm(request.POST, instance=goal)

        if form.is_valid():
            form.save()
            return redirect("goal_list")
        else:
            print(form.errors)

    else:
        form = GoalForm(instance=goal)

    return render(request, "goals/goal_form.html", {"form": form})


def goal_delete(request, pk):
    goal = get_object_or_404(Goal, pk=pk)

    if request.method == "POST":
        goal.delete()
        return redirect("goal_list")

    return render(request, "goals/goal_confirm_delete.html", {"goal": goal})