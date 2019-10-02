from DigiRC.connection import *
from firebase_admin import auth as firebase_admin_auth


def get_user(request):
    return request.session['user']


def get_usertype(request):
    return request.session['usertype']


def get_file_name(request, filename):
    return request.FILES[filename].name


def get_user_details(self, context={}):
    if 'logged_status' in self.request.session:
        user = get_user(self.request)
        usertype = get_usertype(self.request)
        user_info = database.child(str(usertype)).child(str(user['userId'])).child('profile').get()
        if user_info.val() is not None:
            for info in user_info.each():
                context.update({info.key(): info.val()})
    return context


def get_maker_name(self):
    context = get_user_details(self)
    return context.get('company_name')


def already_logged(email):
    try:
        user = firebase_admin_auth.get_user_by_email(email)
        print(user)
        if user is not None:
            return True
        return False
    except:
        return False
