from django import forms
from .models import *


class JarForm(forms.ModelForm):
    class Meta:
        model = Jar
        fields = [
            'jar_name', 'image'
        ]
        widgets = {
            'jar_name': forms.TextInput(attrs={'placeholder': 'Enter jar name'}),

            'image': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
        }

#            'clint_tex': forms.NumberInput(attrs={'placeholder': 'Enter client tax'}),

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = [
            'package_name','package_arabic', 'image'
        ]
        widgets = {
            'package_name': forms.TextInput(attrs={'placeholder': 'Enter bakge name'}),
            'package_arabic': forms.TextInput(attrs={'placeholder': 'Enter bakge name AR '}),

            'image': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
        }


class ProductHamForm(forms.ModelForm):
    class Meta:
        model = ProductHam
        fields = [
            'product_name','top', 'percentage', 'image'
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={'placeholder': 'Enter bakge name'}),
            'top' : forms.NumberInput(attrs={'placeholder': 'Enter the  max kg '}),
            'percentage' : forms.NumberInput(attrs={'placeholder': 'production cost %'}),
            'image': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
        }


class MainProductForm(forms.ModelForm):
    class Meta:
        model = MainProduct
        fields = [
            'product_name', 'product_type', 'product_ham', 'jar', 'package', 
            'image', 'net_weight', 'top_weight', 'amount_inside', 'qr'
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={'placeholder': 'Enter product name'}),
            'product_type': forms.TextInput(attrs={'placeholder': 'Enter product type'}),
            'product_ham': forms.Select(attrs={'class': 'form-control'}),
            'jar': forms.Select(attrs={'class': 'form-control'}),
            'package': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
            'net_weight': forms.NumberInput(attrs={'placeholder': 'Enter the net weight'}),
            'top_weight': forms.NumberInput(attrs={'placeholder': 'Enter the top weight'}),
            'amount_inside': forms.NumberInput(attrs={'placeholder': 'Enter the amount inside'}),
            'qr': forms.NumberInput(attrs={'placeholder': 'Enter product QR'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MainProductForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['product_ham'].queryset = ProductHam.objects.filter(created_by=user.id)
            self.fields['jar'].queryset = Jar.objects.filter(created_by=user.id)
            self.fields['package'].queryset = Package.objects.filter(created_by=user.id)
