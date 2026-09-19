from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


# ==========================
# Register Form
# ==========================
class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "gender",
            "profile_image",
            "password1",
            "password2",
        ]

    def clean(self):
        cleaned_data = super().clean()
        first_name = (cleaned_data.get("first_name") or "").strip()

        if first_name:
            if User.objects.filter(username__iexact=first_name).exists():
                raise forms.ValidationError(
                    "This first name is already in use. Please choose a different name."
                )
            cleaned_data["username"] = first_name

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = (self.cleaned_data.get("first_name") or "").strip()
        if commit:
            user.save()
        return user


# ==========================
# Update Profile Form
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
            "profile_image",
        ]