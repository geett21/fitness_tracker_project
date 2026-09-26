from math import isfinite

from django import forms
from .models import WaterIntake, WaterReminderSettings

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

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if not isfinite(amount) or amount < 0:
            raise forms.ValidationError("Enter a finite, non-negative water amount.")
        return amount


class WaterReminderSettingsForm(forms.ModelForm):
    class Meta:
        model = WaterReminderSettings
        fields = [
            "daily_target_liters",
            "interval_minutes",
            "start_time",
            "end_time",
            "enabled",
        ]
        labels = {
            "daily_target_liters": "Daily water goal (liters)",
            "interval_minutes": "Remind me every",
            "start_time": "Start reminders at",
            "end_time": "Stop reminders at",
            "enabled": "Enable water reminders",
        }
        widgets = {
            "daily_target_liters": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0.25",
                "max": "10",
                "step": "0.25",
            }),
            "interval_minutes": forms.Select(attrs={"class": "form-select"}),
            "start_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "end_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "enabled": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        if start_time and end_time and start_time >= end_time:
            self.add_error("end_time", "End time must be later than the start time.")
        return cleaned_data
