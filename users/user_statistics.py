from DigiRC.connection import *


def user_details(self, context):
    if 'logged_status' in self.request.session:
        user = self.request.session['user']
        user_info = database.child('users').child(str(user['userId'])).child('profile').get()
        if user_info.val() is not None:
            for info in user_info.each():
                context.update({info.key(): info.val()})
    return context


def get_logged_user_list(usertype):
    return database.child('users').child(usertype).get()


def logged_user(users, email):
    if users.val() is not None:
        for user in users.each():
            if user.key().replace(',', '.') == email:
                return True
    return False


def check_user_exists(users, email):
    for user_type in users.each():
        for user_email in user_type.val():
            if user_email.replace(',', '.') == email:
                return True
    return False
