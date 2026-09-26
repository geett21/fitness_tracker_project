from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, EmailMessage
from django.db.models import Sum
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from smtplib import SMTPException
from .forms import PasswordRecoveryForm, RegisterForm, UserUpdateForm
from .models import User
from water.models import WaterIntake, WaterReminderSettings


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
    next_url = (next_url or "").strip()
    if next_url and not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        username = (username or "").strip()
        user = authenticate(request, username=username, password=password)

        if user is None and username and password and "@" in username:
            candidates = User.objects.filter(email__iexact=username, is_active=True)
            if candidates.count() == 1:
                candidate = candidates.first()
                user = authenticate(
                    request,
                    username=candidate.get_username(),
                    password=password,
                )

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


@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")


def password_recovery(request):
    if request.method == "POST":
        form = PasswordRecoveryForm(request.POST)
        if form.is_valid():
            contact = form.cleaned_data["contact"]
            if "@" in contact:
                reset_form = PasswordResetForm({"email": contact})
                if reset_form.is_valid():
                    try:
                        reset_form.save(
                            request=request,
                            use_https=request.is_secure(),
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            email_template_name="usermanagement/password_reset_email.html",
                            subject_template_name="usermanagement/password_reset_subject.txt",
                            token_generator=default_token_generator,
                        )
                    except (BadHeaderError, OSError, SMTPException, ValueError):
                        # Keep the response identical for existing and unknown email addresses.
                        pass
            return redirect("password_reset_done")
    else:
        form = PasswordRecoveryForm()

    return render(request, "usermanagement/forget_password.html", {"form": form})


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
@user_passes_test(lambda user: user.is_staff)
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
@user_passes_test(lambda user: user.is_staff)
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
    reminder_settings, _ = WaterReminderSettings.objects.get_or_create(user=request.user)
    today_total = WaterIntake.objects.filter(
        user=request.user,
        date=timezone.localdate(),
    ).aggregate(total=Sum("amount"))["total"] or 0
    return render(request, "usermanagement/notifications.html", {
        "water_reminders": reminder_settings,
        "water_today_total": today_total,
        "water_remaining": max(float(reminder_settings.daily_target_liters) - float(today_total), 0),
    })


@login_required
def feedback_page(request):
    if request.method == "POST":
        feedback = request.POST.get("message", "").strip()
        if not feedback:
            messages.error(request, "Please enter a message before sending feedback.")
        elif len(feedback) > 5000:
            messages.error(request, "Feedback must be 5,000 characters or fewer.")
        else:
            sender = request.user.get_full_name() or request.user.get_username()
            body = f"Feedback from {sender} ({request.user.email or 'no email provided'}):\n\n{feedback}"
            try:
                email = EmailMessage(
                    subject="Fitness Tracker feedback",
                    body=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.FEEDBACK_EMAIL],
                    reply_to=[request.user.email] if request.user.email else None,
                )
                sent_count = email.send(fail_silently=False)
            except (BadHeaderError, OSError, SMTPException, ValueError):
                sent_count = 0
            if sent_count:
                messages.success(request, "Thanks, your feedback was sent.")
                return redirect("feedback_page")
            messages.error(request, "Feedback could not be sent. Please try again later.")
    return render(request, "usermanagement/feedback.html")


@login_required
def settings_page(request):
    return render(request, "usermanagement/settings.html")
def home(request):
    return redirect("dashboard")
