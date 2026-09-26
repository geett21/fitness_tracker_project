from django import forms
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        max_length=150,
        strip=True,
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "given-name"}),
    )
    last_name = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "family-name"}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "autocomplete": "email"}),
    )
    phone = forms.CharField(
        required=True,
        max_length=15,
        widget=forms.TelInput(attrs={"class": "form-control", "autocomplete": "tel"}),
    )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"].strip()
        if User.objects.filter(username__iexact=first_name).exists():
            raise forms.ValidationError(
                "This username is already in use. Please choose a different first name."
            )
        return first_name

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = "".join(character for character in phone if character.isdigit())
        if (
            not digits
            or len(digits) < 7
            or len(digits) > 15
            or any(character not in "+0123456789 ()-" for character in phone)
            or ("+" in phone and not phone.startswith("+"))
            or phone.count("+") > 1
        ):
            raise forms.ValidationError("Enter a valid phone number with 7 to 15 digits.")
        normalized = ("+" if phone.startswith("+") else "") + digits
        if len(normalized) > 15:
            raise forms.ValidationError("Phone number must contain no more than 15 digits.")
        return normalized

    def clean(self):
        cleaned_data = super().clean()
        first_name = (cleaned_data.get("first_name") or "").strip()
        if first_name:
            cleaned_data["username"] = first_name
            self.instance.username = first_name
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["first_name"].strip()
        if commit:
            user.save()
        return user


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


class PasswordRecoveryForm(forms.Form):
    contact = forms.CharField(
        label="Registered email or phone number",
        max_length=254,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "autocomplete": "email",
            "placeholder": "Email address or phone number",
        }),
    )

    def clean_contact(self):
        contact = self.cleaned_data["contact"].strip()
        if "@" in contact:
            return forms.EmailField().clean(contact)

        digits = "".join(character for character in contact if character.isdigit())
        if (
            not digits
            or len(digits) < 7
            or len(digits) > 15
            or any(character not in "+0123456789 ()-" for character in contact)
            or ("+" in contact and not contact.startswith("+"))
            or contact.count("+") > 1
        ):
            raise forms.ValidationError("Enter a valid email address or phone number.")
        return contact


class PasswordResetSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control", "autocomplete": "new-password"})
