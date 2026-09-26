from math import isfinite

from django import forms
from .models import Goal


class GoalForm(forms.ModelForm):

    class Meta:
        model = Goal

        fields = [
            "goal_type",
            "target_weight",
            "start_date",
            "end_date",
        ]


        widgets = {

            "goal_type": forms.Select(attrs={
                "class": "form-control"
            }),

            "target_weight": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter target weight"
            }),

            "start_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "end_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

        }

    def clean_target_weight(self):
        target_weight = self.cleaned_data["target_weight"]
        if not isfinite(target_weight) or target_weight <= 0:
            raise forms.ValidationError("Target weight must be greater than zero.")
        return target_weight

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date and end_date < start_date:
            self.add_error("end_date", "End date must be on or after the start date.")
        return cleaned_data
