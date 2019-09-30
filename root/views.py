import random
import string
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import FeedbackForm
from DigiRC.connection import *
from firebase_admin import auth

# print(auth.get_user_by_email("shah@gmail.com").uid)

app = settings.APP_NAME

usertypes = ['manufacturer', 'dealer', 'buyer', 'rto']


class Home(TemplateView):
    template_name = 'root/home.html'

    def get_context_data(self, **kwargs):
        context = {'app': app, 'title': 'Home', 'usertypes': usertypes}
        return context


class Contact(TemplateView):
    template_name = 'root/contact.html'

    def get(self, request, *args, **kwargs):
        form = FeedbackForm()
        context = {'app': app, 'title': 'Contact', 'usertypes': usertypes, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback = feedback.__dict__
            for key in {'_state', 'id'}:
                feedback.pop(key)
            try:
                uid = auth.get_user_by_email(feedback.email).uid
                database.child('feedback').child('authenticated').child(str(feedback.email).replace('.', ',')).set(
                    feedback)
                alert = "Your Feedback is Recorded Successfully! We will contact you in few days"
                error = False
            except auth.AuthError:
                database.child('feedback').child('anonymous').child(str(feedback.email).replace('.', ',')).set(
                    feedback)
                alert = "Your Feedback is Recorded Successfully"
                error = False
        else:
            alert = "Enter Valid Details"
            error = True
        return JsonResponse({'alert': alert, 'error': error})


class About(TemplateView):
    template_name = 'root/about.html'

    def get_context_data(self, **kwargs):
        context = {'app': app, 'title': 'About', 'usertypes': usertypes}
        return context
