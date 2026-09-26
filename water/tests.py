from datetime import date, time
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import WaterIntake, WaterReminderSettings


User = get_user_model()


class WaterReminderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="water-user",
            password="StrongTestPassword!42",
            phone="1234567890",
        )
        self.other_user = User.objects.create_user(
            username="other-water-user",
            password="StrongTestPassword!42",
            phone="1234567891",
        )

    def test_reminder_page_requires_login(self):
        response = self.client.get(reverse("water_reminder"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('water_reminder')}",
        )

    def test_reminder_status_requires_login(self):
        response = self.client.get(reverse("water_reminder_status"))
        self.assertEqual(response.status_code, 302)

    def test_user_can_save_settings_and_settings_are_private(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("water_reminder"), {
            "daily_target_liters": "2.50",
            "interval_minutes": "30",
            "start_time": "08:00",
            "end_time": "22:00",
            "enabled": "on",
        })

        self.assertRedirects(response, reverse("water_reminder"))
        settings = WaterReminderSettings.objects.get(user=self.user)
        self.assertEqual(settings.daily_target_liters, Decimal("2.50"))
        self.assertEqual(settings.interval_minutes, 30)
        self.assertTrue(settings.enabled)
        self.assertFalse(WaterReminderSettings.objects.filter(user=self.other_user).exists())

    def test_invalid_interval_and_time_range_are_rejected(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("water_reminder"), {
            "daily_target_liters": "2.00",
            "interval_minutes": "90",
            "start_time": "22:00",
            "end_time": "08:00",
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("interval_minutes", response.context["form"].errors)
        self.assertIn("end_time", response.context["form"].errors)
        saved_settings = WaterReminderSettings.objects.get(user=self.user)
        self.assertFalse(saved_settings.enabled)
        self.assertEqual(saved_settings.interval_minutes, 120)

    def test_status_endpoint_returns_only_current_users_progress(self):
        today = date.today()
        WaterReminderSettings.objects.create(
            user=self.user,
            daily_target_liters=Decimal("2.50"),
            interval_minutes=60,
            start_time=time(8, 0),
            end_time=time(22, 0),
            enabled=True,
        )
        WaterIntake.objects.create(user=self.user, amount=0.75, date=today)
        WaterIntake.objects.create(user=self.other_user, amount=1.50, date=today)
        self.client.force_login(self.user)

        response = self.client.get(reverse("water_reminder_status"), {"date": today.isoformat()})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["today_total"], 0.75)
        self.assertEqual(response.json()["remaining"], 1.75)
        self.assertTrue(response.json()["enabled"])

    def test_notifications_page_renders_current_water_reminder(self):
        WaterReminderSettings.objects.create(user=self.user, enabled=True, interval_minutes=60)
        self.client.force_login(self.user)

        response = self.client.get(reverse("notifications_page"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Water goal: 2.00 L per day")
        self.assertContains(response, reverse("water_reminder"))

    def test_disabling_reminders_stops_status_from_reporting_enabled(self):
        WaterReminderSettings.objects.create(user=self.user, enabled=True)
        self.client.force_login(self.user)
        response = self.client.post(reverse("water_reminder"), {
            "daily_target_liters": "2.00",
            "interval_minutes": "120",
            "start_time": "08:00",
            "end_time": "22:00",
        })

        self.assertRedirects(response, reverse("water_reminder"))
        self.assertFalse(WaterReminderSettings.objects.get(user=self.user).enabled)
        status = self.client.get(reverse("water_reminder_status"))
        self.assertFalse(status.json()["enabled"])


class ExistingWaterTrackerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tracker-user",
            password="StrongTestPassword!42",
            phone="1234567892",
        )
        self.other_user = User.objects.create_user(
            username="tracker-other-user",
            password="StrongTestPassword!42",
            phone="1234567893",
        )
        self.client.force_login(self.user)

    def test_water_list_still_shows_only_current_users_entries(self):
        WaterIntake.objects.create(user=self.user, amount=0.5, date=date.today())
        WaterIntake.objects.create(user=self.other_user, amount=1.0, date=date.today())

        response = self.client.get(reverse("water_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["water"]), list(WaterIntake.objects.filter(user=self.user)))

    def test_existing_water_add_edit_delete_flow_still_works(self):
        response = self.client.post(reverse("water_create"), {
            "amount": "0.5",
            "date": date.today().isoformat(),
            "notes": "After walk",
        })
        self.assertRedirects(response, reverse("water_list"))
        entry = WaterIntake.objects.get(user=self.user)

        response = self.client.post(reverse("water_update", args=[entry.pk]), {
            "amount": "0.75",
            "date": date.today().isoformat(),
            "notes": "Updated",
        })
        self.assertRedirects(response, reverse("water_list"))
        entry.refresh_from_db()
        self.assertEqual(entry.amount, 0.75)
        self.assertEqual(entry.notes, "Updated")

        response = self.client.post(reverse("water_delete", args=[entry.pk]))
        self.assertRedirects(response, reverse("water_list"))
        self.assertFalse(WaterIntake.objects.filter(pk=entry.pk).exists())
