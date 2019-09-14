from django.views.generic import TemplateView, DetailView
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import AddVehicleForm, AddVehicleFileForm
from django.contrib import messages
from django.views import View
import os
import openpyxl
import _csv
import pandas as pd

app = settings.APP_NAME

auth = settings.FIREBASE.auth()

database = settings.FIREBASE.database()


def user_details(request, context):
    if 'logged_status' in request.session:
        user = request.session['user']
        user_info = database.child('users').child(str(user['userId'])).child('details').get()
        if user_info.val() is not None:
            for info in user_info.each():
                context.update({info.key(): info.val()})
    return context


class Dashboard(TemplateView):
    template_name = 'manufacturer/home.html'

    def get_context_data(self, **kwargs):
        context = {'app': app, 'title': 'Dashboard'}
        return context.update(user_details(self.request, context))


def add_vehicle(request):
    form1 = AddVehicleForm()
    form2 = AddVehicleFileForm()
    if request.method == 'POST':
        if 'form1' in request.POST:
            form1 = AddVehicleForm(request.POST)
            if form1.is_valid():
                try:
                    vehicle = form1.save(commit=False)
                    vehicle = vehicle.__dict__
                    for key in ['_state', 'id']:
                        vehicle.pop(key)
                    user = request.session['user']
                    database.child('manufacturer').child(str(user['userId'])).child('vehicles').child(
                        vehicle.get('chassis_no')).set(vehicle)
                    form1 = AddVehicleForm()
                    messages.success(request, f'Saved Successfully')
                except:
                    messages.error(request, f'Error Occured')
            else:
                messages.error(request, f'Details are Invalid')
        elif 'form2' in request.POST and request.FILES['file']:
            form2 = AddVehicleFileForm(request.POST, request.FILES)
            if form2.is_valid():
                if str(request.FILES['file'].name).find('.csv') != -1:
                    try:
                        vehicle_data = form2.save()
                        file_name = request.FILES['file'].name
                        path = os.path.join(settings.BASE_DIR, 'media') + '/datasheets/' + file_name
                        fields = []
                        rows = []
                        with open(path, 'r') as csvfile:
                            # creating a csv reader object
                            csvreader = _csv.reader(csvfile)
                            for row in csvreader:
                                rows.append(row)
                            for field in rows.pop(0):
                                fields.append(field)
                        data_list = []
                        for row in rows:
                            data = {}
                            for (key, value) in zip(fields, row):
                                data.update({key.strip(): value.strip()})
                            data_list.append(data)
                        # print(data_list)
                        user = request.session['user']
                        for vehicle in data_list:
                            database.child('manufacturer').child(str(user['userId'])).child('vehicles').child(
                                vehicle.get('chassis_no')).set(vehicle)
                        os.remove(path)
                        # print('hello')
                        messages.success(request, f'Saved Successfully')
                    except:
                        messages.error(request, f'Error Occured')
                else:
                    messages.error(request, f'Datasheet is not in proper format')
            else:
                messages.error('Invalid File')
    context = {'app': app, 'title': 'Add Vehicle', 'form1': form1, 'form2': form2}
    context.update(user_details(request, context))
    return render(request, 'manufacturer/add.html', context)


class DisplayManufactured(TemplateView):
    template_name = 'manufacturer/manufactured_display.html'

    def get_context_data(self, **kwargs):
        user = self.request.session['user']
        vehicles = database.child('manufacturer').child(str(user['userId'])).child('vehicles').get()
        context = []
        if vehicles.val() is not None:
            for vehicle in vehicles.each():
                context.append(vehicle.val())
        return {'vehicles': context}


class DisplayVehicleDetail(TemplateView):
    template_name = 'manufacturer/vehicle_display.html'

    def get_context_data(self, **kwargs):
        user = self.request.session['user']
        vehicles = database.child('manufacturer').child(str(user['userId'])).child('vehicles').get()
        if vehicles.val() is not None:
            for vehicle in vehicles.each():
                if str(self.request.path).endswith(vehicle.key()):
                    return {'vehicle': vehicle.val()}
