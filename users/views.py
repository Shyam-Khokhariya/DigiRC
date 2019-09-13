import firebase_admin
import os
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from firebase_admin import credentials
from django.contrib import auth as django_auth


app = settings.APP_NAME

auth = settings.FIREBASE.auth()

database = settings.FIREBASE.database()

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
                    return redirect('manu-dashboard')
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


def insurance(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        users = database.child('users').child('insurance').get()
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
                  context={'app': app, 'title': 'Login', 'usertype': 'Insurance Agencies'})


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


def logout(request):
    django_auth.logout(request)
    return render(request, 'users/logout.html', context={'app': app, 'title': 'Logout'})


def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            auth.send_password_reset_email(email)
            messages.success(request, f'Check your email for a link to reset your password. If it doesn’t appear within a few minutes, check your spam folder.')
        except:
            messages.error(request, f'Email address is not registered')
    return render(request, 'users/forgot_password.html', context={'app': app, 'title': 'Password Reset'})

