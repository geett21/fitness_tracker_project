from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from ai_coach import views as ai_coach_views
from usermanagement import views as usermanagement_views
from usermanagement.forms import PasswordResetSetPasswordForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("usermanagement.urls")),
    path("goals/", include("goals.urls")),
    path("water/", include("water.urls")),
    path("weight/", include("weight.urls")),
    path("workout/", include("workout.urls")),
    path("nutrition/", include("nutrition.urls")),
    path("progress/", include("progress.urls")),
    path("ai-coach/", include("ai_coach.urls")),

    # Legacy public names kept for existing bookmarks and integrations.
    path("ai-coach-home/", ai_coach_views.ai_home, name="ai_coach"),
    path("ai-coach-reply/", ai_coach_views.ai_coach_reply, name="ai_coach_reply"),

    path("reports/", include("reports.urls")),

    # Forgot Password
    path("password-reset/", usermanagement_views.password_recovery, name="password_reset"),

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="usermanagement/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="usermanagement/password_reset_confirm.html",
            form_class=PasswordResetSetPasswordForm,
        ),
        name="password_reset_confirm",
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="usermanagement/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),

    path("dashboard/", include("adminlte.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
