import random
import string
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.mail import send_mail
from users.user_statistics import *

app = settings.APP_NAME


def get_requests(request):
    context = list()
    requests = database.child('requests').child('registration').get()
    if requests.val() is not None:
        for i in requests.each():
            print(i.val())
            user = get_user(request)
            user = auth.refresh(user['refreshToken'])
            if i.val().get('usertype') == 'manufacturer':
                email = 'company_email'
            elif i.val().get('usertype') == 'dealer':
                email = 'shop_email'
            else:
                email = 'email'
            license_path = i.val().get('usertype') + "/" + i.val().get(email) + "/" + i.val().get(
                'license')
            logo_path = i.val().get('usertype') + "/" + i.val().get(email) + "/" + i.val().get(
                'logo')
            i.val().update({'license': storage.child(str(license_path)).get_url(user['idToken']),
                            'logo': storage.child(str(logo_path)).get_url(user['idToken'])})
            context.append(i.val())
    return context


class Dashboard(TemplateView):
    template_name = 'rto/home.html'

    def get_context_data(self, **kwargs):
        context = {'app': app, 'title': 'Dashboard'}
        context.update(get_user_details(self, context))
        return context


class RegistrationRequests(TemplateView):
    template_name = 'rto/request.html'

    def get_context_data(self, **kwargs):
        context = {'app': app, 'title': 'Requests'}
        context.update(get_user_details(self, context))
        context.update({'requests': get_requests(self.request)})
        return context


class AcceptRequest(TemplateView):
    template_name = 'rto/accept.html'

    def get(self, request, *args, **kwargs):
        i = str(request.path).rindex('/')
        email = str(request.path)[i + 1:]
        letters = string.ascii_letters + string.digits
        passwordLength = 8
        password = ''.join(random.choice(letters) for i in range(passwordLength))
        req = database.child('requests').child('registration').child(email.replace('.', ',')).get()
        context = dict()
        for i in req.each():
            context.update({i.key(): i.val()})
        subject = 'DigiRC Login Credentials'
        message = 'Hello Sir,\n your registration request for DigiRC is accepted successfully\n \n Your Login ' \
                  'Credentials are:\n Email: ' + email + '\nPassword: ' + password + '\nDon\'t share this ' \
                                                                                     'credentials with anyone.'
        from_email = str(settings.EMAIL_HOST_USER)
        to = list()
        to.append(email)
        send_mail(subject, message, from_email, to, auth_user='digirc2019@gmail.com',
                  auth_password='digirc!@#$19', fail_silently=False)
        user = auth.create_user_with_email_and_password(email, password)
        uid = user['localId']
        users = database.child('users').child(str(context.get('usertype'))).get()
        users_list = dict()
        if users.val() is not None:
            for i in users.each():
                users_list.update({i.key(): i.val()})
        users_list.update({email.replace('.', ','): str(uid)})
        database.child('users').child(str(context.get('usertype'))).set(users_list)
        database.child(str(context.get('usertype'))).child(str(uid)).child('profile').set(context)
        database.child('requests').child('registration').child(email.replace('.', ',')).remove()
        messages.success(request, f'Account Credentials are sent to email')
        return redirect('rto-registration-requests')


class RejectRequest(TemplateView):
    template_name = 'rto/reject.html'

    def get(self, request, *args, **kwargs):
        i = str(request.path).rindex('/')
        email = str(request.path)[i + 1:]
        subject = 'Regarding Request Rejection'
        message = 'Hello Sir,\n your registration request for DigiRC is rejected because your documents were not ' \
                  'correct.\nPlease provide correct documents for registration. '
        from_email = str(settings.EMAIL_HOST_USER)
        to = list()
        to.append(email)
        send_mail(subject, message, from_email, to, auth_user='digirc2019@gmail.com',
                  auth_password='digirc!@#$19', fail_silently=False)
        database.child('requests').child('registration').child(email.replace('.', ',')).remove()
        return redirect('rto-registration-requests')
