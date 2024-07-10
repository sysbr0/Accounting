# forms.py
from django import forms
from .models import *

class ClintsForm(forms.ModelForm):
    class Meta:
        model = clints
        fields = [
            'clint_name', 'clint_tex', 'clint_email', 'c_number', 'c_sorce',
            'clint_iban', 'is_company', 'clint_tr_name', 'image'
        ]
        widgets = {
            'clint_name': forms.TextInput(attrs={'placeholder': 'Enter client name'}),
            'clint_tex': forms.NumberInput(attrs={'placeholder': 'Enter client tax'}),
            'clint_email': forms.EmailInput(attrs={'placeholder': 'Enter client email'}),
            'c_number': forms.TextInput(attrs={'placeholder': 'Enter contact number'}),
            'c_sorce': forms.TextInput(attrs={'placeholder': 'Enter client source'}),
            'clint_iban': forms.TextInput(attrs={'placeholder': 'Enter IBAN'}),
            'is_company': forms.CheckboxInput(attrs={'placeholder': 'Is it a company?'}),
            'clint_tr_name': forms.TextInput(attrs={'placeholder': 'Enter trade name'}),
            'image': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
        }
