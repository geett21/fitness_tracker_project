from django.urls import path
from . import views

urlpatterns = [
    # Register, Login, Logout
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # CRUD
    path("", views.home, name="home"),
    path("users/", views.user_list, name="user_list"),
    path("add/", views.user_create, name="user_create"),
    path("update/<int:id>/", views.user_update, name="user_update"),
    path("delete/<int:id>/", views.user_delete, name="user_delete"),
    path("base/", views.base, name="base"),
    path("profile/", views.profile, name="profile"),
    path("notifications/", views.notifications_page, name="notifications_page"),
    path("feedback/", views.feedback_page, name="feedback_page"),
    path("settings/", views.settings_page, name="settings_page"),
]
