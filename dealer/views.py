from users.user_statistics import *
from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

app = settings.APP_NAME


class Dashboard(TemplateView):
    template_name = 'dealer/home.html'

    def get_context_data(self, **kwargs):
        # user = get_user(self.request)
        # vehicles = database.child('dealer').child(str(user['userId'])).child('vehicles').get()
        context = {'app': app, 'title': 'Dashboard'}
        # chart1(vehicles, context)
        # print(context)
        context.update(get_user_details(self, context))
        # print(context)
        return context


class DeliveryList(TemplateView):
    template_name = 'dealer/delivery_list.html'
    
    def get(self, request, *args, **kwargs):
        try:
            context = {'app': app, 'title': 'Deliveries'}
            context.update(get_user_details(self, context))
            vehicle_data = get_vehicle_alloted(self.request)
            print(len(list(vehicle_data.keys())))
            data_list = []
            for i in range(0, len(list(vehicle_data.keys()))):            
                manufacturer_id = list(vehicle_data.keys())[i]
                print(manufacturer_id)
                manu_name = vehicle_data.get(manufacturer_id).get('manufacturer_name')
                print(manu_name)
                chassis_list = vehicle_data.get(manufacturer_id).get('chassis_list')
                print(chassis_list)
                date_time = vehicle_data.get(manufacturer_id).get('date_time')
                print(date_time)
                data_list.append({'manufacturer_id': manufacturer_id, 'manufacturer_name': manu_name, 'chassis_list': chassis_list, 'date_time': date_time})
            context.update({'data_list': data_list})
        except:
            pass
        return render(request, self.template_name, context)


class Accept(TemplateView):
    template_name = 'dealer/accept.html'
    
    def get(self, request, *args, **kwargs):
        # try:
            print(kwargs['pk'])
            user = request.session['user']
            manu_id = kwargs['pk']
            data = database.child('requests').child('chassis_alloted').child(str(user['userId'])).child(manu_id).get()
            if data.val() is not None:
                chassis_list = data.val().get('chassis_list')
                date_time = data.val().get('date_time')
                manufacturer_name = data.val().get('manufacturer_name')
                vehicle_list = list()
                for chassis in chassis_list:
                    database.child('manufacturer').child(manu_id).child('vehicles').child(chassis).child('delivery_status').set('delivered')
                    vehicle = dict(database.child('manufacturer').child(manu_id).child('vehicles').child(chassis).get().val())
                    database.child('dealer').child(str(user['userId'])).child('vehicles').child(chassis).set(vehicle)
                date = datetime.now().strftime("%d_%m_%Y")
                database.child('manufacturer').child(manu_id).child('delivered').child(str(user['userId'])).child(str(date)).set(chassis_list)
                database.child('requests').child('chassis_alloted').child(str(user['userId'])).child(manu_id).remove()
                return redirect('delivery-list')
            else:
                print('error')
                messages.error(request, f'Database Error')
        # except:
        #     print('exception')
        #     messages.error(request, f'Error In Accepting Request')
            return render(request, self.template_name)
    

class Reject(TemplateView):
    template_name = 'dealer/reject.html'

    def get(self, request, *args, **kwargs):
        print(kwargs['pk'])
        user = request.session['user']
        manu_id = kwargs['pk']
        database.child('requests').child('chassis_alloted').child(str(user['userId'])).child(manu_id).remove()
        return render(request, self.template_name)
