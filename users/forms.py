from django import forms
from root.models import Manufacturer


class RegisterManufacturerForm(forms.ModelForm):

    class Meta:
        model = Manufacturer
        fields = ['name', 'email', 'contact', 'industry_license']
