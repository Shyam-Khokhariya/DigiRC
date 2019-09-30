import json
from django.template import RequestContext
from DigiRC.connection import *
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth as django_auth
from .forms import *
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from .user_statistics import *

app = settings.APP_NAME


def process_login(request, usertype):
    try:
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.sign_in_with_email_and_password(email, password)
        user = auth.refresh(user['refreshToken'])
        request.session['logged_status'] = True
        request.session['user'] = user
        request.session['usertype'] = usertype
        return True
    except:
        return False


def login(request, usertype):
    form = LoginForm()
    if request.method == 'POST':
        if process_login(request, usertype):
            path = str(usertype).lower() + "-dashboard"
            return redirect(path)
        else:
            form = LoginForm(request.POST)
            messages.error(request, f'Invalid Credentials')
    return render(request, 'users/login.html',
                  context={'app': app, 'title': 'Login', 'usertype': usertype, 'form': form})


# Registration Form for all Users
def register(request, usertype):
    if usertype == 'rto':
        return redirect('home')
    if request.method == 'POST':
        if usertype == 'manufacturer':
            form = RegisterManufacturerForm(request.POST)
        elif usertype == 'dealer':
            form = RegisterDealerForm(request.POST)
        else:
            form = RegisterBuyerForm(request.POST)
        if form.is_valid():
            try:
                email = request.POST.get('email')
                # Retrieve Registered Users List
                users = database.child('users').get()
                if not check_user_exists(users, email):
                    file_name = request.FILES['industry_license']
                    if str(file_name).find('.jpeg') == -1 and str(file_name).find('.jpg') == -1 and str(file_name).find(
                            '.png') == -1:
                        messages.error(request, f'License Must be in JPG/PNG Format')
                    else:
                        user = form.save()
                        user = user.__dict__
                        for key in {'_state', 'id'}:
                            user.pop(key)
                        # Make path to local user directory for uploaded license
                        path = os.path.join(settings.BASE_DIR, 'media') + "/" + str(user.get('industry_license'))
                        if str(file_name).find('.jpg') != -1:
                            file_name = 'license.jpg'
                        elif str(file_name).find('.jpeg') != -1:
                            file_name = 'license.jpeg'
                        else:
                            file_name = 'license.png'
                        user.update({'industry_license': file_name, 'usertype': 'manufacturer'})
                        # Upload license in firebase storage
                        storage.child('manufacturer').child(str(user.get('email'))).child(str(file_name)).put(path)
                        # Upload Data in firebase Database
                        database.child('requests').child('registration').child(
                            str(user.get('email')).replace('.', ',')).set(user)
                        # Remove Image From Uploaded Directory
                        os.remove(path)
                        messages.success(request, f'Applied for Registration')
                else:
                    messages.error(request, f'Email Already Registered')
            except:
                messages.error(request, f'System Error')
        else:
            messages.error(request, f'Invalid Details')
    else:
        if usertype == 'manufacturer':
            form = RegisterManufacturerForm()
        elif usertype == 'dealer':
            form = RegisterDealerForm()
        else:
            form = RegisterBuyerForm()
    return render(request, 'users/register.html',
                  context={'app': app, 'title': 'Register', 'usertype': usertype, 'form': form})


# Logout User
def logout(request):
    context = {'app': app, 'title': 'Logout', 'usertype': str(request.session['usertype'])}
    django_auth.logout(request)
    return render(request, 'users/logout.html', context)


# Forgot Password
def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            auth.send_password_reset_email(email)
            messages.success(request,
                             f'Check your email for a link to reset your password. If it doesn’t appear within a few '
                             f'minutes, check your spam folder.')
        except:
            messages.error(request, f'Email address is not registered')
    return render(request, 'users/forgot_password.html', context={'app': app, 'title': 'Password Reset'})
