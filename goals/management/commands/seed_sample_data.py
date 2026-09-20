from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from goals.models import Goal
from water.models import WaterIntake
from weight.models import WeightTracker, SleepTracker, StepTracker

import datetime


class Command(BaseCommand):
    help = "Seed the database with sample fitness data"

    def handle(self, *args, **options):
        User = get_user_model()

        # Create sample user if none exist
        if not User.objects.filter(username="sampleuser").exists():
            user = User.objects.create_user("sampleuser", email="sample@example.com", password="password123")
            self.stdout.write(self.style.SUCCESS("Created sample user: sampleuser / password123"))
        else:
            user = User.objects.get(username="sampleuser")
            self.stdout.write(self.style.NOTICE("Sample user already exists"))

        today = datetime.date.today()

        # Create a sample goal
        if not Goal.objects.exists():
            Goal.objects.create(goal_type="Weight Loss", target_weight=70.0, start_date=today - datetime.timedelta(days=30), end_date=today + datetime.timedelta(days=60))
            self.stdout.write(self.style.SUCCESS("Created sample Goal"))
        else:
            self.stdout.write(self.style.NOTICE("Goals already present"))

        # Water entries
        if not WaterIntake.objects.exists():
            WaterIntake.objects.create(amount=2.0, date=today - datetime.timedelta(days=1), notes="Evening")
            WaterIntake.objects.create(amount=1.5, date=today, notes="Morning")
            self.stdout.write(self.style.SUCCESS("Created sample WaterIntake entries"))
        else:
            self.stdout.write(self.style.NOTICE("Water entries already present"))

        # Weight / steps / sleep
        if not WeightTracker.objects.exists():
            WeightTracker.objects.create(user=user, weight=80.0, height=175.0, goal='Loss')
            StepTracker.objects.create(user=user, steps=5000)
            SleepTracker.objects.create(user=user, sleep_hours=7.5)
            self.stdout.write(self.style.SUCCESS("Created sample Weight, Step, and Sleep entries"))
        else:
            self.stdout.write(self.style.NOTICE("Weight/Step/Sleep entries already present"))

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
