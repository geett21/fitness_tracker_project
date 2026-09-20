from django import forms
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


class SleepForm(forms.ModelForm):
    class Meta:
        model = SleepTracker
        fields = ['sleep_hours']


class StepForm(forms.ModelForm):
    class Meta:
        model = StepTracker
        fields = ['steps']
