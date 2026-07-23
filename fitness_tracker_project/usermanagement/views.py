from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from .models import User


# ==========================
# REGISTER
# ==========================
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "usermanagement/register.html", {
        "form": form
    })


# ==========================
# LOGIN
# ==========================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "usermanagement/login.html", {
                "error_message": "Invalid username or password."
            })

    return render(request, "usermanagement/login.html")


# ==========================
# READ (List Users)
# ==========================
def user_list(request):
    users = User.objects.all()
    return render(request, "usermanagement/user_list.html", {
        "users": users
    })


# ==========================
# CREATE (Add User)
# ==========================
def user_create(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("user_list")

    else:
        form = RegisterForm()

    return render(request, "usermanagement/user_form.html", {
        "form": form
    })


# ==========================
# UPDATE (Edit User)
# ==========================
def user_update(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        form = RegisterForm(
            request.POST,
            request.FILES,
            instance=user
        )

        if form.is_valid():
            form.save()
            return redirect("user_list")

    else:
        form = RegisterForm(instance=user)

    return render(request, "usermanagement/user_form.html", {
        "form": form
    })


# ==========================
# DELETE (Delete User)
# ==========================
def user_delete(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        user.delete()
        return redirect("user_list")

    return render(request, "usermanagement/user_delete.html", {
        "user": user
    })

def base(request):
    return render(request, "base.html")
