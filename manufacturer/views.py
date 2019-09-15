from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import AddVehicleForm, AddVehicleFileForm
from django.contrib import messages
import os
import _csv

app = settings.APP_NAME

auth = settings.FIREBASE.auth()

database = settings.FIREBASE.database()


def get_user(request):
    return request.session['user']


def user_details(request, context):
    if 'logged_status' in request.session:
        user = get_user(request)
        user_info = database.child('manufacturer').child(str(user['userId'])).child('profile').get()
        if user_info.val() is not None:
            for info in user_info.each():
                context.update({info.key(): info.val()})
    return context


class Dashboard(TemplateView):
    template_name = 'manufacturer/home.html'

    def get_context_data(self, **kwargs):
        context = {'app': app, 'title': 'Dashboard'}
        context.update(user_details(self.request, context))
        return context


def get_file_name(request, file_name):
    return request.FILES[file_name].name


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
                    user = get_user(request)
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
                if str(get_file_name(request, 'file')).find('.csv') != -1:
                    try:
                        form2.save()
                        file_name = get_file_name(request, 'file')
                        path = os.path.join(settings.BASE_DIR, 'media') + '/datasheets/' + file_name
                        fields = list()
                        rows = list()
                        with open(path, 'r') as csvfile:
                            csvreader = _csv.reader(csvfile)
                            for row in csvreader:
                                rows.append(row)
                            for field in rows.pop(0):
                                fields.append(field)
                        data_list = list()
                        for row in rows:
                            data = dict()
                            for (key, value) in zip(fields, row):
                                data.update({key.strip(): value.strip()})
                            data_list.append(data)
                        user = get_user(request)
                        for vehicle in data_list:
                            database.child('manufacturer').child(str(user['userId'])).child('vehicles').child(
                                vehicle.get('chassis_no')).set(vehicle)
                        os.remove(path)
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
        user = get_user(self.request)
        vehicles = database.child('manufacturer').child(str(user['userId'])).child('vehicles').get()
        context = list()
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
