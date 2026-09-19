from django import forms
from .models import WaterIntake

class WaterIntakeForm(forms.ModelForm):

    class Meta:
        model = WaterIntake

        fields = [
            "amount",
            "date",
            "notes",
        ]

        widgets = {
            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Water Intake (Liters)"
            }),

            "date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Optional Notes"
            }),
        }