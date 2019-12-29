from django import forms
from .models import *


class SignalForm(forms.ModelForm):
    class Meta:
        model = Signal
        fields = ['periodStart', 'periodEnd', 'equation']
        labels = {
            'periodStart': 'ابتدای بازه',
            'periodEnd': 'انتهای بازه',
            'equation': 'معادله سیگنال'
        }
        widgets = {
            'periodStart': forms.TextInput(attrs={'placeholder': '-5'}),
            'periodEnd': forms.TextInput(attrs={'placeholder': '5'}),
            'equation': forms.TextInput(attrs={'placeholder': 'u(t+2)-u(t-2)'})
        }
        fields_order= ['periodStart', 'periodEnd', 'equation']