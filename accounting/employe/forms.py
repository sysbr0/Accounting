# forms.py
from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'position', 'age', 'tc', 'title', 'state']  # Specify which fields you want in the form
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'ادخل الاسم'}),
            'position': forms.TextInput(attrs={'placeholder': 'ادخل الوظيفة'}),
            'age': forms.NumberInput(attrs={'placeholder': 'العمر'}),
            'tc': forms.TextInput(attrs={'placeholder': 'رقم الهوية'}),
            'title': forms.TextInput(attrs={'placeholder': 'اللقب'}),
            'state': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'activeCheck'}),  # Example for checkbox input with custom class
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})