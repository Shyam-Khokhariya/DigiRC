import firebase_admin
import os
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from firebase_admin import credentials
from django.contrib import auth as django_auth
from .forms import RegisterManufacturerForm

app = settings.APP_NAME

auth = settings.FIREBASE.auth()

database = settings.FIREBASE.database()

storage = settings.FIREBASE.storage()

filepath = os.path.join(settings.BASE_DIR, 'DigiRC\\service_account_key.json')
cred = credentials.Certificate(filepath)
firebase_admin.initialize_app(cred)


def user_details(self, context):
    if 'logged_status' in self.request.session:
        user = self.request.session['user']
        user_info = database.child('users').child(str(user['userId'])).child('details').get()
        if user_info.val() is not None:
            for info in user_info.each():
                context.update({info.key(): info.val()})
    return context


def new_user(users, email):
    if users.val() is not None:
        for user in users.each():
            if user.key().replace(',', '.') == email:
                return True
    return False


def manufacturer(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        users = database.child('users').child('manufacturer').get()
        if new_user(users, email):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                user = auth.refresh(user['refreshToken'])
                session_id = user['idToken']
                request.session['uid'] = str(session_id)
                request.session['logged_status'] = True
                request.session['user'] = user
                request.session['usertype'] = 'manufacturer'
                return redirect('manu-dashboard')
            except:
                messages.error(request, f'Invalid Credentials')
        else:
            messages.error(request, f'Invalid Email or Password')
    return render(request, 'users/login.html',
                  context={'app': app, 'title': 'Login', 'usertype': 'Manufacturer'})


def dealer(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        users = database.child('users').child('dealer').get()
        if new_user(users, email):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                user = auth.refresh(user['refreshToken'])
                session_id = user['idToken']
                request.session['uid'] = str(session_id)
                request.session['logged_status'] = True
                request.session['user'] = user
                request.session['usertype'] = 'dealer'
                return redirect('home')
            except:
                messages.error(request, f'Invalid Credentials')
        else:
            messages.error(request, f'Invalid Email or Password')
    return render(request, 'users/login.html',
                  context={'app': app, 'title': 'Login', 'usertype': 'Dealer'})


def buyer(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        users = database.child('users').child('customer').get()
        if new_user(users, email):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                user = auth.refresh(user['refreshToken'])
                session_id = user['idToken']
                request.session['uid'] = str(session_id)
                request.session['logged_status'] = True
                request.session['user'] = user
                request.session['usertype'] = 'customer'
                return redirect('home')
            except:
                messages.error(request, f'Invalid Credentials')
        else:
            messages.error(request, f'Invalid Email or Password')
    return render(request, 'users/login.html',
                  context={'app': app, 'title': 'Login', 'usertype': 'Buyer'})


def insurance(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        users = database.child('users').child('insurance').get()
        if new_user(users, email):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                user = auth.refresh(user['refreshToken'])
                session_id = user['idToken']
                request.session['uid'] = str(session_id)
                request.session['logged_status'] = True
                request.session['user'] = user
                request.session['usertype'] = 'insurance'
                return redirect('home')
            except:
                messages.error(request, f'Invalid Credentials')
        else:
            messages.error(request, f'Invalid Email or Password')
    return render(request, 'users/login.html',
                  context={'app': app, 'title': 'Login', 'usertype': 'Insurance Agencies'})


def rto(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        users = database.child('users').child('rto').get()
        if new_user(users, email):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                user = auth.refresh(user['refreshToken'])
                session_id = user['idToken']
                request.session['uid'] = str(session_id)
                request.session['logged_status'] = True
                request.session['user'] = user
                request.session['usertype'] = 'rto'
                return redirect('rto-dashboard')
            except:
                messages.error(request, f'Invalid Credentials')
        else:
            messages.error(request, f'Invalid Email or Password')
    return render(request, 'users/login.html',
                  context={'app': app, 'title': 'Login', 'usertype': 'RTO Officer'})


def register(request):
    if request.method == 'POST':
        form = RegisterManufacturerForm(request.POST, request.FILES)
        if form.is_valid():
            email = request.POST.get('email')
            users = database.child('users').get()
            flag = True
            for user_type in users.each():
                for user_email in user_type.val():
                    if user_email.replace(',', '.') == email:
                        flag = False
            if flag:
                file_name = request.FILES['industry_license']
                if str(file_name).find('.jpg') == -1 and str(file_name).find('.png') == -1:
                    messages.error(request, f'License Must be in JPG/PNG Format')
                else:
                    try:
                        user = form.save()
                        user = user.__dict__
                        for key in {'_state', 'id'}:
                            user.pop(key)
                        path = os.path.join(settings.BASE_DIR, 'media') + "/" + str(user.get('industry_license'))
                        if str(file_name).find('.jpg') != -1:
                            file_name = 'license.jpg'
                        else:
                            file_name = 'license.png'
                        user.update({'industry_license': file_name, 'usertype': 'manufacturer'})
                        storage.child('manufacturer').child(str(user.get('email'))).child(str(file_name)).put(path)
                        database.child('requests').child('registration').child(
                            str(user.get('email')).replace('.', ',')).set(user)
                        os.remove(path)
                        messages.success(request, f'Applied for Registration')
                    except:
                        messages.error(request, f'System Error')
            else:
                messages.error(request, f'Email Already Registered')
        else:
            messages.error(request, f'Invalid Details')
    else:
        form = RegisterManufacturerForm()
    return render(request, 'users/register.html', context={'app': app, 'title': 'Register', 'form': form})


def logout(request):
    context = {'app': app, 'title': 'Logout'}
    if str(request.session['usertype']) == 'manufacturer':
        context.update({'log_url': 'manu-login'})
    elif str(request.session['usertype']) == 'dealer':
        context.update({'log_url': 'dealer-login'})
    elif str(request.session['usertype']) == 'customer':
        context.update({'log_url': 'buyer-login'})
    elif str(request.session['usertype']) == 'insurance':
        context.update({'log_url': 'insurance-login'})
    elif str(request.session['usertype']) == 'rto':
        context.update({'log_url': 'rto-login'})
    django_auth.logout(request)
    return render(request, 'users/logout.html', context)


def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            auth.send_password_reset_email(email)
            messages.success(request,
                             f'Check your email for a link to reset your password. If it doesn’t appear within a few minutes, check your spam folder.')
        except:
            messages.error(request, f'Email address is not registered')
    return render(request, 'users/forgot_password.html', context={'app': app, 'title': 'Password Reset'})
