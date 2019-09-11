from django.shortcuts import redirect, render
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import messages

app = settings.APP_NAME

auth = settings.FIREBASE.auth()

database = settings.FIREBASE.database()


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
