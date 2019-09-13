from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import AddVehicleForm, AddVehicleFileForm
from django.contrib import messages
from django.views import View
import openpyxl, os

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
                    print(vehicle)
                    user = request.session['user']
                    database.child('manufacturer').child(str(user['userId'])).child('vehicles').child().set(vehicle)
                except:
                    messages.error(request, f'Error Occured')
            else:
                messages.error(request, f'Details are Invalid')
        elif 'form2' in request.POST and request.FILES['xls_file']:
            form2 = AddVehicleFileForm(request.POST, request.FILES)
            if form2.is_valid():
                vehicle_data = form2.save()
                print(request.FILES['xls_file'].name)
                path = os.path.join(settings.BASE_DIR, 'media') + '/datasheets/' + request.FILES['xls_file'].name
                wb = openpyxl.load_workbook(path, read_only=True)

                # getting a particular sheet by name out of many sheets
                worksheet = wb.active
                print(worksheet)

                excel_data = list()
                # iterating over the rows and
                # getting value from each cell in row
                for row in worksheet.iter_rows():
                    row_data = list()
                    for cell in row:
                        row_data.append(str(cell.value))
                    excel_data.append(row_data)
                print(excel_data)
            else:
                messages.error('Invalid File')
    context = {'app': app, 'title': 'Add Vehicle', 'form1': form1, 'form2': form2}
    context.update(user_details(request, context))
    return render(request, 'manufacturer/add.html', context)
