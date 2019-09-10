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


def user_details(self):
    context = {'app': app, 'title': 'Home'}
    if 'logged_status' in self.request.session:
        user = self.request.session['user']
        user_info = database.child('users').child(str(user['userId'])).child('details').get()
        for info in user_info.each():
            context.update({info.key(): info.val()})
    return context


class Home(TemplateView):
    template_name = 'root/home.html'

    def get_context_data(self, **kwargs):
        return user_details(self)


class About(TemplateView):
    template_name = 'root/about.html'

    def get_context_data(self, **kwargs):
        return user_details(self)
