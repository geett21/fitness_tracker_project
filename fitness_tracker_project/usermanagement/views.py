from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .forms import RegisterForm, UserUpdateForm
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

    return render(request, "usermanagement/user_form.html", {
        "form": form,
        "is_registration": True,
    })


# ==========================
# LOGIN
# ==========================
def login_view(request):
    next_url = request.GET.get("next", "") or request.POST.get("next", "")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        username = (username or "").strip()
        user = authenticate(request, username=username, password=password)

        if user is None and username and password:
            candidate = User.objects.filter(
                Q(username__iexact=username) | Q(first_name__iexact=username),
                is_active=True,
            ).first()
            if candidate and candidate.check_password(password):
                if not candidate.username and candidate.first_name:
                    candidate.username = candidate.first_name.strip()
                    candidate.save(update_fields=["username"])
                user = candidate

        if user is not None:
            login(request, user)
            return redirect(next_url or "dashboard")
        else:
            return render(request, "login.html", {
                "error_message": "Invalid username or password.",
                "next": next_url,
            })

    return render(request, "login.html", {
        "next": next_url,
    })


def logout_view(request):
    logout(request)
    return redirect("login")


# ==========================
# READ (List Users)
# ==========================
@user_passes_test(lambda user: user.is_staff)
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

@login_required
def user_update(request, id):

    user = get_object_or_404(User, id=id)
    if user != request.user and not request.user.is_staff:
        return redirect("profile")

    if request.method == "POST":

        form = UserUpdateForm(
            request.POST,
            request.FILES,
            instance=user
        )

        if form.is_valid():
            form.save()
            return redirect("profile")

    else:

        form = UserUpdateForm(instance=user)


    return render(request,
                  "usermanagement/user_form.html",
                  {
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

@login_required
def profile(request):
    return render(request, "usermanagement/profile.html", {
        "user": request.user
    })


@login_required
def notifications_page(request):
    return render(request, "usermanagement/notifications.html")


@login_required
def feedback_page(request):
    return render(request, "usermanagement/feedback.html")


@login_required
def settings_page(request):
    return render(request, "usermanagement/settings.html")
def home(request):
    return redirect("dashboard")
