from django.shortcuts import redirect, reverse
from django.conf import settings
from django.views.generic import TemplateView

app = settings.APP_NAME

# auth = settings.FIREBASE.auth()

database = settings.FIREBASE.database()


def page_not_found(request, exception):
    if len(request.path[0:request.path.rindex("/")]) == 0:
        return redirect('home')
    else:
        return redirect(request.path[0:request.path.rindex("/")])


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
