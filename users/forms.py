from django import forms
from manufacturer.models import Manufacturer
from dealer.models import Dealer
from buyer.models import Buyer


class RegisterManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['company_name', 'owner_name', 'company_email', 'company_contact', 'owner_contact', 'license_no',
                  'address', 'city', 'state', 'company_logo', 'company_license']


class RegisterDealerForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = ['shop_name', 'owner_name', 'shop_email', 'shop_contact', 'owner_contact', 'license_no',
                  'address', 'city', 'state', 'shop_logo', 'shop_license']


class RegisterBuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['name', 'father_name', 'husband_name', 'gender', 'age', 'address', 'city', 'state', 'birth_place',
                  'email', 'contact1', 'contact2', 'license_no', 'profile_pic', 'driving_license']


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
