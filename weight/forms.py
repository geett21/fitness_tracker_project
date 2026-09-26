from django import forms
from math import isfinite

from .models import WeightTracker, SleepTracker, StepTracker


class WeightForm(forms.ModelForm):

    class Meta:
        model = WeightTracker

        fields = [
            'weight',
            'height',
            'goal',
        ]

        widgets = {
            'weight': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter weight in kg'
                }
            ),

            'height': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter height in cm'
                }
            ),

            'goal': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

    def clean_weight(self):
        weight = self.cleaned_data["weight"]
        if not isfinite(weight) or weight <= 0:
            raise forms.ValidationError("Weight must be greater than zero.")
        return weight

    def clean_height(self):
        height = self.cleaned_data["height"]
        if not isfinite(height) or height <= 0:
            raise forms.ValidationError("Height must be greater than zero.")
        return height


class SleepForm(forms.ModelForm):
    class Meta:
        model = SleepTracker
        fields = ['sleep_hours']


class StepForm(forms.ModelForm):
    class Meta:
        model = StepTracker
        fields = ['steps']
