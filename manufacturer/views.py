from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import AddVehicleForm
from django.contrib import messages
from django.views import View

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
    if request.method == 'POST':
        if 'form1' in request.POST:
            form = AddVehicleForm(request.POST)
            if form.is_valid():
                vehicle = form.save(commit=False)
                vehicle = vehicle.__dict__
                for key in ['_state', 'id']:
                    vehicle.pop(key)
                print(vehicle)
                user = request.session['user']
                user_info = database.child('manufacturer').child(str(user['userId'])).child('vehicles').child().set(vehicle)
                database.child('manufacturer').child('')
            else:
                messages.error(request, f'Details are Invalid')
        elif 'form2' in request.POST:
            file = request.FILES['xls_file']

    else:
        form = AddVehicleForm()
    context = {'app': app, 'title': 'Add Vehicle', 'form': form}
    context.update(user_details(request, context))
    return render(request, 'manufacturer/add.html', context)
