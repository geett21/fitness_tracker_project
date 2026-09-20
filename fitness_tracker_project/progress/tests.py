from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from weight.models import WeightTracker


class ProgressViewTests(TestCase):
    def test_progress_page_shows_weight_chart_data(self):
        user = get_user_model().objects.create_user(
            username="tester",
            password="secret123"
        )

        WeightTracker.objects.create(
            user=user,
            weight=70.5,
            height=175,
            goal="Maintain",
            date=timezone.now().date() - timedelta(days=1),
        )
        WeightTracker.objects.create(
            user=user,
            weight=69.5,
            height=175,
            goal="Maintain",
            date=timezone.now().date(),
        )

        self.client.force_login(user)
        response = self.client.get(reverse("progress_home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "weightChart")
        self.assertIn("dates", response.context)
        self.assertEqual(response.context["weight_values"], [70.5, 69.5])
