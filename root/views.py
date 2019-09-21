from django.conf import settings
from django.views.generic import TemplateView
from .forms import FeedbackForm
from django.shortcuts import render
import random
import string

app = settings.APP_NAME

auth = settings.FIREBASE.auth()

database = settings.FIREBASE.database()

usertypes = ['Manufacturer', 'Dealer', 'Buyer', 'RTO']


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
        try:
            form = FeedbackForm(request.POST)
            feedback = form.save(commit=False)
            feedback = feedback.__dict__
            print(feedback)
            for key in {'_state', 'id'}:
                feedback.pop(key)
            letters = string.ascii_letters + string.digits
            print(letters)
            uidLength = 16
            uid = ''.join(random.choice(letters) for i in range(uidLength))
            database.child('feedback').child('anonymous').child(uid).set(feedback)
            alert = "Your Feedback is Recorded Successfully"
        except:
            alert = "Some Error Occured"
        context = {'app': app, 'title': 'Contact', 'usertypes': usertypes, 'form': form, 'alert': alert}
        return render(request, self.template_name, context)


class About(TemplateView):
    template_name = 'root/about.html'

    def get_context_data(self, **kwargs):
        context = {'app': app, 'title': 'About', 'usertypes': usertypes}
        return context
