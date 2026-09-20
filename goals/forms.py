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