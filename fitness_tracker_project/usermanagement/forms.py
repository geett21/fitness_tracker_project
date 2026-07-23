from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


# ==========================
# Register Form
# ==========================
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "gender",
            "address",
            "profile_image",
            "password1",
            "password2",
        ]


# ==========================
# Update Form
# ==========================
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "gender",
            "address",
            "profile_image",
        ]