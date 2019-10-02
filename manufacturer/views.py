import _csv
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import AddVehicleForm, AddVehicleFileForm
from users.user_statistics import *

app = settings.APP_NAME


class Dashboard(TemplateView):
    template_name = 'manufacturer/home.html'

    def get_context_data(self, **kwargs):
        context = {'app': app, 'title': 'Dashboard'}
        context.update(get_user_details(self, context))
        return context


def chassis_added(vehicle, user):
    vehicle_data = database.child('manufacturer').child(str(user['userId'])).child('vehicles').child(
        vehicle.get('chassis_no')).get()
    if vehicle_data.val() is not None:
        return True
    else:
        return False


class AddVehicle(TemplateView):
    template_name = 'manufacturer/add.html'

    def get(self, request, *args, **kwargs):
        form1 = AddVehicleForm(initial={'maker': str(get_maker_name(self))})
        form2 = AddVehicleFileForm()
        context = {'app': app, 'title': 'Add Vehicle', 'form1': form1, 'form2': form2}
        context.update(get_user_details(self, context))
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form1 = AddVehicleForm()
        form2 = AddVehicleFileForm()
        if 'form1' in request.POST:
            form1 = AddVehicleForm(request.POST)
            if form1.is_valid():
                try:
                    vehicle = form1.save(commit=False)
                    vehicle = vehicle.__dict__
                    for key in ['_state', 'id']:
                        vehicle.pop(key)
                    user = get_user(request)
                    if chassis_added(vehicle, user):
                        messages.error(request, f'Chassis No Already Added')
                    else:
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
                    form2.save()
                    file_name = get_file_name(request, 'file')
                    print(file_name)
                    path = os.path.join(settings.BASE_DIR, 'media') + '/datasheets/' + file_name
                    print(path)
                    fields = list()
                    rows = list()
                    print(path)
                    with open(path, 'r') as csvfile:
                        print('hello')
                        csvreader = _csv.reader(csvfile)
                        for row in csvreader:
                            print(row)
                            rows.append(row)
                        for field in rows.pop(0):
                            fields.append(field)
                    data_list = list()
                    for row in rows:
                        data = dict()
                        for (key, value) in zip(fields, row):
                            data.update({key.strip(): value.strip()})
                        data_list.append(data)
                    print(data_list)
                    user = get_user(request)
                    print(user)
                    for vehicle in data_list:
                        database.child('manufacturer').child(str(user['userId'])).child('vehicles').child(
                            vehicle.get('chassis_no')).set(vehicle)
                    print('done')
                    os.remove(path)
                    messages.success(request, f'Saved Successfully')
                else:
                    messages.error(request, f'Datasheet is not in proper format')
            else:
                messages.error(request, f'Invalid File')
        context = {'app': app, 'title': 'Add Vehicle', 'form1': form1, 'form2': form2}
        context.update(get_user_details(self, context))
        return render(request, self.template_name, context)



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
                    if chassis_added(vehicle, user):
                        messages.error(request, f'Chassis No Already Added')
                    else:
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
    context.update(get_user_details(request, context))
    return render(request, 'manufacturer/add.html', context)


class DisplayManufactured(TemplateView):
    template_name = 'manufacturer/manufactured_display.html'

    def get_context_data(self, **kwargs):
        user = get_user(self.request)
        vehicles = database.child('manufacturer').child(str(user['userId'])).child('vehicles').get()
        vehicles_list = list()
        if vehicles.val() is not None:
            for vehicle in vehicles.each():
                vehicles_list.append(vehicle.val())
        context = {'app': app, 'title': 'Display Vehicles'}
        context.update(get_user_details(self, context))
        paginator = Paginator(vehicles_list, settings.VEHICLE_COUNT)
        page = self.request.GET.get('page')
        vehicles = paginator.get_page(page)
        print(vehicles)
        context.update({'vehicles': vehicles})
        return context


class DisplayVehicleDetail(TemplateView):
    template_name = 'manufacturer/vehicle_display.html'

    def get_context_data(self, **kwargs):
        user = self.request.session['user']
        vehicles = database.child('manufacturer').child(str(user['userId'])).child('vehicles').get()
        context = {'app': app, 'title': 'Display Vehicles'}
        context.update(get_user_details(self, context))
        if vehicles.val() is not None:
            for vehicle in vehicles.each():
                if str(self.request.path).endswith(vehicle.key()):
                    context.update({'vehicle': vehicle.val()})
                    break
        return context
