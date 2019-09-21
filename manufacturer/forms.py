from django import forms
from root.models import ManufacturerVehicleInfo, ManufacturerVehicleDataSheet
import datetime

month = [(i, j) for (i, j) in
         zip(range(1, 13),
             ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November',
              'December'])]

year = [(i, i) for i in range(1901, 2101)]
current_year = datetime.date.today().year
current_month = month[datetime.date.today().month-1]
fuel = [(i, i) for i in ['Petrol', 'Diesel', 'CNG']]
vehicle_class_choice = [(i, i) for i in ['Light Vehicles', 'Medium Heavy Vehicles', 'Large Heavy Vehicles',
                                         'Extra Large Heavy Vehicles']]


class AddVehicleForm(forms.ModelForm):
    chassis_no = forms.CharField(label='Chassis Number')
    engine_no = forms.CharField(label='Engine Number')
    fuel_type = forms.ChoiceField(label='Type of Fuel', choices=fuel)
    maker = forms.CharField(label='Maker\'s Name')
    model = forms.CharField(label='Model Name')
    vehicle_class = forms.CharField(label='Class of vehicle')
    body_type = forms.CharField(label='Type of Body')
    vehicle_type = forms.CharField(label='Type of Vehicle')
    manufacture_month = forms.ChoiceField(label='Manufacturing Month', choices=month, initial=current_month)
    manufacture_year = forms.ChoiceField(label='Manufacturing Year', choices=year, initial=current_year)
    number_of_cylinders = forms.CharField(label='No. of Cylinders')
    horse_power = forms.CharField(label='Horse Power')
    cubic_capacity = forms.CharField(label='Cubic Capacity')  # CC of Vehicle
    wheel_base = forms.CharField(label='Wheel Base')  # distance between front and rear axles of vehicle in mm
    seating_capacity = forms.CharField(label='Seating Capacity')
    unladen_weight = forms.CharField(label='Unladen weight')  # Weight of Vehicle when not loaded with goods
    color = forms.CharField(label='Color')
    price = forms.CharField(label='Price')

    class Meta:
        model = ManufacturerVehicleInfo
        fields = ['chassis_no', 'engine_no', 'fuel_type', 'maker', 'model', 'vehicle_class', 'body_type',
                  'vehicle_type', 'manufacture_month', 'manufacture_year', 'number_of_cylinders', 'horse_power',
                  'cubic_capacity', 'wheel_base', 'seating_capacity', 'unladen_weight', 'color', 'price']


class AddVehicleFileForm(forms.ModelForm):
    file = forms.FileField(label='Upload Datasheet')

    class Meta:
        model = ManufacturerVehicleDataSheet
        fields = ['file']
