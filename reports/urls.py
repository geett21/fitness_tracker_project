from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("", views.reports_dashboard, name="dashboard"),
    path("weekly/", views.weekly_report, name="weekly"),
    path("monthly/", views.monthly_report, name="monthly"),
    path("weekly/pdf/", views.weekly_pdf, name="weekly_pdf"),
    path("monthly/pdf/", views.monthly_pdf, name="monthly_pdf"),
]
