import firebase_admin
import os
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from firebase_admin import credentials
from django.contrib import auth as django_auth
from django.views.generic import TemplateView


app = settings.APP_NAME

# auth = settings.FIREBASE.auth()

database = settings.FIREBASE.database()

filepath = os.path.join(settings.BASE_DIR, 'DigiRC\\service_account_key.json')
cred = credentials.Certificate(filepath)
firebase_admin.initialize_app(cred)


def user_details(self, context):
    if 'logged_status' in self.request.session:
        user = self.request.session['user']
        user_info = database.child('users').child(str(user['userId'])).child('details').get()
        if user_info is not None:
            for info in user_info.each():
                context.update({info.key(): info.val()})
    return context


def login(request):
    usernames = database.child['usernames'].get()
    for username in usernames.each():
        print(username.key() + ": " + username.val())
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            pass
            # # user = auth.sign_in_with_email_and_password(email, password)
            # # user = auth.refresh(user['refreshToken'])
            # session_id = user['idToken']
            # request.session['uid'] = str(session_id)
            # request.session['logged_status'] = True
            # request.session['user'] = user
            # print(request.session['user'])
            # return redirect('home')
        except:
            messages.error(request, f'Invalid Credentials')
    return render(request, 'users/login.html',
                  context={'app': app, 'title': 'Login'})


def logout(request):
    django_auth.logout(request)
    return render(request, 'users/logout.html', context={'app': app, 'title': 'Logout'})
