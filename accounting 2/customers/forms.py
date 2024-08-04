# forms.py
from django import forms
from .models import *

class CostomersForm(forms.ModelForm):
    class Meta:
        model = Costomers
        fields = [
            'name', 'email', 'number', 'address'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter client name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter client email'}),
            'number': forms.TextInput(attrs={'placeholder': 'Enter contact number'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter client source'}),
              }




class CostomersFormAdvanv(forms.ModelForm):
    class Meta:
        model = Costomers
        fields = [
            'name', 'tex', 'email', 'number', 'address',
            'is_company', 'company', 'image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter name'}),
            'tex': forms.NumberInput(attrs={'placeholder': 'Enter tax'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
            'number': forms.TextInput(attrs={'placeholder': 'Enter contact number'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter address'}),
            'is_company': forms.CheckboxInput(attrs={'placeholder': 'Is it a company?'}),
            'company': forms.TextInput(attrs={'placeholder': 'Enter company name'}),
            'image': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
            'token': forms.TextInput(attrs={'readonly': 'readonly', 'style': 'background-color: lightgray;'}),
        }

    def __init__(self, *args, **kwargs):
        super(CostomersFormAdvanv, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CostomersFormAdvanv, self).save(commit=False)
        # Generate token if it's not provided
        if not instance.token:
            instance.generate_token()  # Replace with your token generation logic
        if commit:
            instance.save()
        return instance
    



    