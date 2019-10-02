from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import auth as django_auth
from .forms import *
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


# Registration Form for Manufacturer
def manu_register(request):
    if request.method == 'POST':
        form = RegisterManufacturerForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                email = request.POST.get('company_email')
                print(email)
                if not already_logged(email):
                    users = database.child('requests').child('registration').get()
                    print(users)
                    if users.val() is not None:
                        messages.error(request, f'Already Applied for Registration, We will contact you in 1 or 2 days')
                    else:
                        print('hello')
                        file_name1 = request.FILES['company_license']
                        file_name2 = request.FILES['company_logo']
                        if str(file_name1).find('.jpeg') == -1 and str(file_name1).find('.jpg') == -1 and str(
                                file_name1).find(
                                '.png') == -1:
                            messages.error(request, f'License Must be in JPG/PNG Format')
                        elif str(file_name2).find('.jpeg') == -1 and str(file_name2).find('.jpg') == -1 and str(
                                file_name2).find('.png') == -1:
                            messages.error(request, f'Logo Must be in JPG/PNG Format')
                        else:
                            user = form.save()
                            user = user.__dict__
                            # Make path to local user directory for uploaded license
                            print(user)
                            path1 = os.path.join(settings.BASE_DIR, 'media') + "/" + str(user.get('company_license'))
                            path2 = os.path.join(settings.BASE_DIR, 'media') + "/" + str(user.get('company_logo'))
                            if str(file_name1).find('.jpg') != -1:
                                file_name1 = 'license.jpg'
                            elif str(file_name1).find('.jpeg') != -1:
                                file_name1 = 'license.jpeg'
                            else:
                                file_name1 = 'license.png'
                            if str(file_name2).find('.jpg') != -1:
                                file_name2 = 'logo.jpg'
                            elif str(file_name2).find('.jpeg') != -1:
                                file_name2 = 'logo.jpeg'
                            else:
                                file_name2 = 'logo.png'
                            for key in {'_state', 'id', 'company_license', 'company_logo'}:
                                user.pop(key)
                            print(user)
                            user.update(
                                {'license': file_name1, 'logo': file_name2, 'usertype': 'manufacturer'})
                            print(user)
                            # Upload license in firebase storage
                            storage.child('manufacturer').child(str(email)).child(str(file_name1)).put(path1)
                            storage.child('manufacturer').child(str(email)).child(str(file_name2)).put(path2)
                            print('uploaded')
                            # Upload Data in firebase Database
                            database.child('requests').child('registration').child(
                                str(email).replace('.', ',')).set(user)
                            print('databse done')
                            # Remove Image From Uploaded Directory
                            os.remove(path1)
                            os.remove(path2)
                            messages.success(request, f'Applied for Registration')
                else:
                    messages.error(request, f'Email Already Registered! Try to login')
            except:
                messages.error(request, f'System Error')
        else:
            print(form.errors)
            messages.error(request, f'Invalid Details')
    else:
        form = RegisterManufacturerForm()
    return render(request, 'users/register.html',
                  context={'app': app, 'title': 'Register', 'usertype': 'manufacturer', 'form': form})


def dealer_register(request):
    if request.method == 'POST':
        form = RegisterDealerForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                email = request.POST.get('email')
                if already_logged(email):
                    users = database.child('requests').child('registration').child(str(email)).get()
                    if users.val() is None:
                        file_name1 = request.FILES['shop_license']
                        file_name2 = request.FILES['shop_logo']
                        if str(file_name1).find('.jpeg') == -1 and str(file_name1).find('.jpg') == -1 and str(
                                file_name1).find(
                                '.png') == -1:
                            messages.error(request, f'License Must be in JPG/PNG Format')
                        elif str(file_name2).find('.jpeg') == -1 and str(file_name2).find('.jpg') == -1 and str(
                                file_name2).find('.png') == -1:
                            messages.error(request, f'Logo Must be in JPG/PNG Format')
                        else:
                            user = form.save()
                            user = user.__dict__
                            # Make path to local user directory for uploaded license
                            path1 = os.path.join(settings.BASE_DIR, 'media') + "/" + str(user.get('shop_license'))
                            path2 = os.path.join(settings.BASE_DIR, 'media') + "/" + str(user.get('shop_logo'))
                            if str(file_name1).find('.jpg') != -1:
                                file_name1 = 'license.jpg'
                            elif str(file_name1).find('.jpeg') != -1:
                                file_name1 = 'license.jpeg'
                            else:
                                file_name1 = 'license.png'
                            if str(file_name2).find('.jpg') != -1:
                                file_name2 = 'logo.jpg'
                            elif str(file_name2).find('.jpeg') != -1:
                                file_name2 = 'logo.jpeg'
                            else:
                                file_name2 = 'logo.png'
                            for key in {'_state', 'id', 'shop_license', 'shop_logo'}:
                                user.pop(key)
                            user.update(
                                {'license': file_name1, 'logo': file_name2, 'usertype': 'dealer'})
                            # Upload license in firebase storage
                            storage.child('dealer').child(str(user.get('email'))).child(str(file_name1)).put(path1)
                            storage.child('dealer').child(str(user.get('email'))).child(str(file_name2)).put(path2)
                            # Upload Data in firebase Database
                            database.child('requests').child('registration').child(
                                str(user.get('email')).replace('.', ',')).set(user)
                            # Remove Image From Uploaded Directory
                            os.remove(path1)
                            os.remove(path2)
                            messages.success(request, f'Applied for Registration')
                    else:
                        messages.error(request, f'Already Applied for Registration, We will contact you in 1 or 2 days')
                else:
                    messages.error(request, f'Email Already Registered! Try to login')
            except:
                messages.error(request, f'System Error')
        else:
            print(form.errors)
            messages.error(request, f'Invalid Details')
    else:
        form = RegisterDealerForm()
    return render(request, 'users/register.html',
                  context={'app': app, 'title': 'Register', 'usertype': 'dealer', 'form': form})


def buyer_register(request):
    if request.method == 'POST':
        form = RegisterBuyerForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                email = request.POST.get('email')
                if already_logged(email):
                    users = database.child('requests').child('registration').child(str(email)).get()
                    if users.val() is None:
                        file_name1 = request.FILES['driving_license']
                        file_name2 = request.FILES['profile_pic']
                        if str(file_name1).find('.jpeg') == -1 and str(file_name1).find('.jpg') == -1 and str(
                                file_name1).find(
                                '.png') == -1:
                            messages.error(request, f'License Must be in JPG/PNG Format')
                        elif str(file_name2).find('.jpeg') == -1 and str(file_name2).find('.jpg') == -1 and str(
                                file_name2).find('.png') == -1:
                            messages.error(request, f'Logo Must be in JPG/PNG Format')
                        else:
                            user = form.save()
                            user = user.__dict__
                            # Make path to local user directory for uploaded license
                            path1 = os.path.join(settings.BASE_DIR, 'media') + "/" + str(user.get('driving_license'))
                            path2 = os.path.join(settings.BASE_DIR, 'media') + "/" + str(user.get('profile_pic'))
                            if str(file_name1).find('.jpg') != -1:
                                file_name1 = 'license.jpg'
                            elif str(file_name1).find('.jpeg') != -1:
                                file_name1 = 'license.jpeg'
                            else:
                                file_name1 = 'license.png'
                            if str(file_name2).find('.jpg') != -1:
                                file_name2 = 'profile.jpg'
                            elif str(file_name2).find('.jpeg') != -1:
                                file_name2 = 'profile.jpeg'
                            else:
                                file_name2 = 'profile.png'
                            for key in {'_state', 'id', 'driving_license', 'profile_pic'}:
                                user.pop(key)
                            user.update(
                                {'license': file_name1, 'logo': file_name2, 'usertype': 'buyer'})
                            # Upload license in firebase storage
                            storage.child('buyer').child(str(user.get('email'))).child(str(file_name1)).put(path1)
                            storage.child('buyer').child(str(user.get('email'))).child(str(file_name2)).put(path2)
                            # Upload Data in firebase Database
                            database.child('requests').child('registration').child(
                                str(user.get('email')).replace('.', ',')).set(user)
                            # Remove Image From Uploaded Directory
                            os.remove(path1)
                            os.remove(path2)
                            messages.success(request, f'Applied for Registration')
                    else:
                        messages.error(request, f'Already Applied for Registration, We will contact you in 1 or 2 days')
                else:
                    messages.error(request, f'Email Already Registered! Try to login')
            except:
                messages.error(request, f'System Error')
        else:
            print(form.errors)
            messages.error(request, f'Invalid Details')
    else:
        form = RegisterBuyerForm()
    return render(request, 'users/register.html',
                  context={'app': app, 'title': 'Register', 'usertype': 'buyer', 'form': form})


# Logout User
def logout(request):
    try:
        context = {'app': app, 'title': 'Logout', 'usertype': str(request.session['usertype'])}
        django_auth.logout(request)
        return render(request, 'users/logout.html', context)
    except:
        return redirect('home')


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
