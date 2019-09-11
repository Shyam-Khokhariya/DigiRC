from django.shortcuts import redirect, render
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import messages

app = settings.APP_NAME

auth = settings.FIREBASE.auth()

database = settings.FIREBASE.database()


def get_vehicles(self):
    context = {}
    if 'logged_status' in self.request.session:
        user = self.request.session['user']
        vehicles_info = database.child('users').child(str(user['userId'])).child('vehicles').get()
        vehicle = {}
        for vehicles in vehicles_info:
            vehicle.clear()
            for info in vehicles:
                vehicle.update({info.key(): info.val()})
            context.update({vehicles.key(): vehicle})
            print(context)
    return context


def user_details(self, context):
    if 'logged_status' in self.request.session:
        user = self.request.session['user']
        user_info = database.child('users').child(str(user['userId'])).child('details').get()
        if user_info.val() is not None:
            for info in user_info.each():
                context.update({info.key(): info.val()})
    return context


class Home(TemplateView):
    template_name = 'root/home.html'

    def get_context_data(self, **kwargs):
        return user_details(self, context={'app': app, 'title': 'Home'})


class Contact(TemplateView):
    template_name = 'root/contact.html'

    def get_context_data(self, **kwargs):
        return user_details(self, context={'app': app, 'title': 'Contact'})


def manufacturer(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        users = database.child('users').child('manufacturer').get()
        for user in users.each():
            if user.key().replace(',', '.') == email:
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    user = auth.refresh(user['refreshToken'])
                    session_id = user['idToken']
                    request.session['uid'] = str(session_id)
                    request.session['logged_status'] = True
                    request.session['user'] = user
                    return redirect('home')
                except:
                    messages.error(request, f'Invalid Credentials')
                    break
    return render(request, 'users/login.html',
                  context={'app': app, 'title': 'Login', 'usertype': 'Manufacturer'})


def dealer(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        users = database.child('users').child('dealer').get()
        for user in users.each():
            if user.key().replace(',', '.') == email:
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    user = auth.refresh(user['refreshToken'])
                    session_id = user['idToken']
                    request.session['uid'] = str(session_id)
                    request.session['logged_status'] = True
                    request.session['user'] = user
                    return redirect('home')
                except:
                    messages.error(request, f'Invalid Credentials')
                    break
    return render(request, 'users/login.html',
                  context={'app': app, 'title': 'Login', 'usertype': 'Dealer'})


def buyer(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        users = database.child('users').child('customer').get()
        for user in users.each():
            if user.key().replace(',', '.') == email:
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    user = auth.refresh(user['refreshToken'])
                    session_id = user['idToken']
                    request.session['uid'] = str(session_id)
                    request.session['logged_status'] = True
                    request.session['user'] = user
                    return redirect('home')
                except:
                    messages.error(request, f'Invalid Credentials')
                    break
    return render(request, 'users/login.html',
                  context={'app': app, 'title': 'Login', 'usertype': 'Buyer'})


def rto(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        users = database.child('users').child('rto').get()
        for user in users.each():
            if user.key().replace(',', '.') == email:
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    user = auth.refresh(user['refreshToken'])
                    session_id = user['idToken']
                    request.session['uid'] = str(session_id)
                    request.session['logged_status'] = True
                    request.session['user'] = user
                    return redirect('home')
                except:
                    messages.error(request, f'Invalid Credentials')
                    break
    return render(request, 'users/login.html',
                  context={'app': app, 'title': 'Login', 'usertype': 'RTO Officer'})
