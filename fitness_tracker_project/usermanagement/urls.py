from django.urls import path
from . import views

urlpatterns = [
    # Register & Login
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),

    # CRUD
    path("", views.user_list, name="user_list"),
    path("add/", views.user_create, name="user_create"),
    path("update/<int:id>/", views.user_update, name="user_update"),
    path("delete/<int:id>/", views.user_delete, name="user_delete"),
    path("base/", views.base, name="base"),
]