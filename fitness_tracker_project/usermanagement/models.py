
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    phone = models.CharField(max_length=15)

    address = models.TextField(blank=True)

    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=10,
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
        ],
        blank=True
    )

    def __str__(self):
        return self.username