from django import forms
from manufacturer.models import Manufacturer
from dealer.models import Dealer
from buyer.models import Buyer
from DigiRC.connection import *


def get_brand_names(brand_names):
    try:
        manu = database.child('manufacturer').get()
        if manu.val() is not None:
            for manufacturer in manu.each():
                brand_names.append((manufacturer.val().get('profile').get('company_name'), manufacturer.val().get(
                    'profile').get('company_name')))
            return brand_names
    except ConnectionError:
        print('no connection')
        return brand_names


# brand_names = [('Select Brand Name', 'Select Brand Name')]
brand_list = get_brand_names(brand_names=[])
# print(brand_names)


class RegisterManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['company_name', 'owner_name', 'company_email', 'company_contact', 'owner_contact', 'license_no',
                  'address', 'city', 'state', 'company_logo', 'company_license']


class RegisterDealerForm(forms.ModelForm):
    authorized_dealer = forms.BooleanField(label='Mark Here if you are a authorized dealer?')
    authorized_brand = forms.ChoiceField(choices=brand_list, required=False)
    brand_names = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}) ,required=False)

    class Meta:
        model = Dealer
        fields = ['shop_name', 'owner_name', 'shop_email', 'shop_contact', 'owner_contact', 'license_no',
                  'address', 'city', 'state', 'authorized_dealer', 'authorized_brand', 'brand_names', 'shop_logo',
                  'shop_license']


class RegisterBuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['name', 'father_name', 'husband_name', 'gender', 'age', 'address', 'city', 'state', 'birth_place',
                  'email', 'contact1', 'contact2', 'aadhar_no', 'license_no', 'profile_pic', 'driving_license']


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
