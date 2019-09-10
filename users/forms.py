from django import forms
from .models import UserData


class SignUpForm(forms.ModelForm):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = UserData
        fields = ['name', 'email', 'mobile', 'password']
