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
        # print(user)
        if user is not None:
            return True
        return False
    except:
        return False


def get_dealers():
    dealer_list = []
    dealers = database.child("dealer").get()
    if dealers.val() is not None:
        for dealer in dealers.each():
            dealer_name = dealer.val().get('profile').get('shop_name')
            dealer_list.append((dealer_name, dealer_name))
        # print(dealer_list)
    return dealer_list


def get_dealer_id(name):
    dealers = database.child("dealer").get()
    # print(dealers.val())
    if dealers.val() is not None:
        for dealer in dealers.each():
            if str(dealer.val().get('profile').get('shop_name')) == str(name):
                id = dealer.__dict__.get('item')[0]
                # print(id)
                return id


def get_vehicles(request, chassis_list):
    # try:
    vehicle_list = list()
    user = request.session['user']
    vehicles = database.child('manufacturer').child(str(user['userId'])).child('vehicles').get()
    if vehicles.val() is not None:
        for vehicle in vehicles.each():
            if str(vehicle.__dict__.get('item')[0]) in chassis_list:
                vehicle_list.append({vehicle.__dict__.get(
                    'item')[0]: vehicle.__dict__.get('item')[1]})
    # print(vehicle_list)
    # except:
        # print('exception')
    return vehicle_list


def get_vehicle_alloted(request):
    user = request.session['user']
    # get vehicle from request
    vehicle_data = database.child('requests').child('chassis_alloted').child(str(user['userId'])).get()
    if vehicle_data.val() is not None:
        vehicle_data = dict(vehicle_data.val())
        return vehicle_data
    else:
        return None
        
