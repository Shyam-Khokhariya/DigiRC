import _csv
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import AddVehicleForm, AddVehicleFileForm, DealerAssignForm
from users.user_statistics import *
from collections import OrderedDict
from datetime import datetime

from django.shortcuts import render, redirect
from .fusioncharts import FusionCharts
import pandas as pd

app = settings.APP_NAME


def get_range(chassis_alloted):
    # print(chassis_alloted)
    min_max = str(chassis_alloted).split('-')
    # print(min_max)
    i = int(str(min_max[0])[8:])
    j = int(str(min_max[1])[8:])
    # print(i)
    # print(j)
    prefix = str(min_max[0])[:8]
    # print(prefix)
    if i < j:
        chassis_list = [str(prefix) + str(k).zfill(4)
                        for k in range(i, j+1)]
    else:
        chassis_list = [str(prefix) + str(k).zfill(4)
                        for k in range(j, i+1)]
    return chassis_list

def remove_duplicates_from_list(data_list):
    return list(dict.fromkeys(data_list))

def chart1(vehicles, context):
    dataSource = {}
    data = pd.DataFrame()
    for v in vehicles.each():
        # print(v.val())
        data = data.append(pd.DataFrame([v.val()]))
    # print(data.columns)
    context['data1'] = data
    # print(context['data1'])
    chartConfig = {
        "borderColor": "#ffffff",
        "bgColor": "#ffffff",
        "borderAlpha": "80",
        "theme": "fusion",
        "xAxisName": "Vehicle Type",
        "yAxisName": "Sales",
        "palettecolors": "#cbe86d,#a8d3ed,#ffcd8c,#ffabdd",

        "showRealTimeValue": "0",

    }

    # The `chartData` dict contains key-value pairs data
    chartData = {}

    u_body_type = data.body_type.unique()
    list_body_type = list(data.body_type)
    # print(u_body_type)
    for d in u_body_type:
        chartData[d] = list_body_type.count(d)
    # print(chartData)
    dataSource["chart"] = chartConfig
    dataSource["data"] = []

    for key, value in chartData.items():
        data1 = {}
        data1["label"] = key
        data1["value"] = value
        dataSource["data"].append(data1)

    column2D = FusionCharts("column2d", "ex", "100%", "120%", "chart-1", "json", dataSource)
    context['output'] = column2D.render()
    # return (column2D.render())
    veh_chartConfig = {
        "palettecolors": "#d9fcf8",
        "showLabels": "0",
        "showYAxisValues": "0",
        "showBorder": "0",
        "theme": "fusion",
        "showPlotBorder": "1",
        "drawFullAreaBorder": "0",
        "usePlotGradientColor": "2",
        "plotBorderThickness": "2",
        "plotBorderColor": "#00c0c0",
        "canvasPadding": "-50px",
        "showRealTimeValue": "0",
        "plotGradientColor": "#00ffe2"
    }
    total_vehicle1 = {}
    total_vehicle1["chart"] = veh_chartConfig
    total_vehicle1["categories"] = [{
        "category": [
        ]
    }]

    total_vehicle1["dataset"] = [{"data": [
    ]
    }
    ]
    total_vehicle1["data"] = []
    print(total_vehicle1["categories"][0]["category"])
    year = data.manufacture_year.unique()
    year.sort()
    total_vehicle1["categories"][0]["category"].append({"label": (str)(int(year[0]) - 1)})
    total_vehicle1["dataset"][0]["data"].append({"value": 0})
    # print(year)
    for y in year:
        total_vehicle1["categories"][0]["category"].append({"label": y})
    # print(total_vehicle["categories"][0]["category"])
    for d in year:
        total_vehicle1["dataset"][0]["data"].append({"value": list(data.manufacture_year).count(d)})

    chartObj1 = FusionCharts('stackedarea2d', 'ex1', '100%', '100%', 'Total_vehicle1', 'json', total_vehicle1)
    context['op_tot1'] = chartObj1.render()

    veh_chartConfig2 = {
        "palettecolors": "#ffd000",
        "showLabels": "1",
        "showYAxisValues": "1",
        "xAxisName": "Year",
        "yAxisName": "Number Of Vehicle Manufactured",
        "yAxisMinValue": "0",
        "xAxisMinValue": "0",
        "showBorder": "0",
        "theme": "fusion",
        "showPlotBorder": "1",
        "drawFullAreaBorder": "0",
        "usePlotGradientColor": "3",
        "plotBorderThickness": "2",
        "plotBorderColor": "#ff0303",
        "canvasPadding": "30",
        "showValues": "1",
        "showRealTimeValue": "0",
        "plotGradientColor": "#f7fa98"
    }
    total_vehicle1["chart"] = veh_chartConfig2
    chartObj2 = FusionCharts('stackedarea2d', 'ex2', '100%', '180%', 'Total_vehicle2', 'json', total_vehicle1)
    context['op_tot2'] = chartObj2.render()
    growth = (total_vehicle1["dataset"][0]["data"][-1]["value"] - total_vehicle1["dataset"][0]["data"][-2]["value"]) / \
             total_vehicle1["dataset"][0]["data"][-2]["value"]
    context['Growth'] = round(growth * 100, 2)

    print(data.status.unique())

    chartConfig = {
        "numberPrefix": "$",
        "defaultCenterLabel": "Total revenue: $64.08K",
        "centerLabel": "Revenue from $label: $value",
        "pieRadius": "40%",
        "labelDistance": "10px",
        "doughnutRadius": "200%",
        "enableSmartLabels": "1",
        "manageLabelOverflow": "1",
        "labelPosition": "Outside",
        "showPercentInToolTip": "1",
        "useEllipsesWhenOverflow": "1",
        "theme": "fusion"
    }

    # The `chartData` dict contains key-value pairs data
    chartData = {}
    u_body_type = data.body_type.unique()
    list_body_type = list(data.body_type)
    # print(u_body_type)
    for d in u_body_type:
        chartData[d] = list_body_type.count(d)
    # print(chartData)
    dataSource["chart"] = chartConfig
    dataSource["data"] = []

    for key, value in chartData.items():
        data1 = {}
        data1["label"] = key
        data1["value"] = value
        dataSource["data"].append(data1)

    Dough = FusionCharts("doughnut2d", "do", "100%", "300%", "dough", "json", dataSource)
    context['op_dough'] = Dough.render()


# template - home.html
class Dashboard(TemplateView):
    template_name = 'manufacturer/home.html'

    def get_context_data(self, **kwargs):
        user = get_user(self.request)
        vehicles = database.child('manufacturer').child(str(user['userId'])).child('vehicles').get()
        context = {'app': app, 'title': 'Dashboard'}
        chart1(vehicles, context)
        # print(context)
        context.update(get_user_details(self, context))
        # print(context)
        return context


def chassis_added(vehicle, user):
    vehicle_data = database.child('manufacturer').child(str(user['userId'])).child('vehicles').child(
        vehicle.get('chassis_no')).get()
    if vehicle_data.val() is not None:
        return True
    else:
        return False


# template - add.html
class AddVehicle(TemplateView):
    template_name = 'manufacturer/add.html'

    def get(self, request, *args, **kwargs):
        form1 = AddVehicleForm(initial={'maker': str(get_maker_name(self))})
        form2 = AddVehicleFileForm()
        context = {'app': app, 'title': 'Add Vehicle', 'form1': form1, 'form2': form2}
        context.update(get_user_details(self, context))
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form1 = AddVehicleForm()
        form2 = AddVehicleFileForm()
        if 'form1' in request.POST:
            form1 = AddVehicleForm(request.POST)
            if form1.is_valid():
                try:
                    vehicle = form1.save(commit=False)
                    vehicle = vehicle.__dict__
                    for key in ['_state', 'id']:
                        vehicle.pop(key)
                    user = get_user(request)
                    if chassis_added(vehicle, user):
                        messages.error(request, f'Chassis No Already Added')
                    else:
                        vehicle.update({'delivery_status': 'undelivered'})
                        database.child('manufacturer').child(str(user['userId'])).child('vehicles').child(
                            vehicle.get('chassis_no')).set(vehicle)
                        form1 = AddVehicleForm()
                        messages.success(request, f'Saved Successfully')
                except:
                    messages.error(request, f'Error Occured')
            else:
                messages.error(request, f'Details are Invalid')
        elif 'form2' in request.POST and request.FILES['file']:
            form2 = AddVehicleFileForm(request.POST, request.FILES)
            if form2.is_valid():
                if str(get_file_name(request, 'file')).find('.csv') != -1:
                    form2.save()
                    file_name = get_file_name(request, 'file')
                    print(file_name)
                    path = os.path.join(settings.BASE_DIR, 'media') + '/datasheets/' + file_name
                    # print(path)
                    fields = list()
                    rows = list()
                    try:
                        with open(path, 'r') as csvfile:
                            csvreader = _csv.reader(csvfile)
                            for row in csvreader:
                                rows.append(row)
                            for field in rows.pop(0):
                                fields.append(field)
                        data_list = list()
                        for row in rows:
                            data = dict()
                            for (key, value) in zip(fields, row):
                                data.update({key.strip(): value.strip()})
                            data_list.append(data)
                        print(data_list)
                        user = get_user(request)
                        print(user)
                        for vehicle in data_list:
                            vehicle.update({'delivery_status': 'undelivered'})
                            database.child('manufacturer').child(str(user['userId'])).child('vehicles').child(
                                vehicle.get('chassis_no')).set(vehicle)
                        print('done')
                        os.remove(path)
                        messages.success(request, f'Saved Successfully')
                    except:
                        print('exception')
                        os.remove(path)
                else:
                    messages.error(request, f'Datasheet is not in proper format')
            else:
                messages.error(request, f'Invalid File')
        context = {'app': app, 'title': 'Add Vehicle', 'form1': form1, 'form2': form2}
        context.update(get_user_details(self, context))
        return render(request, self.template_name, context)


# template - manufactured_display.html
class DisplayManufactured(TemplateView):
    template_name = 'manufacturer/manufactured_display.html'

    def get_context_data(self, *args, **kwargs):
        user = get_user(self.request)
        vehicles = database.child('manufacturer').child(str(user['userId'])).child('vehicles').get()
        vehicles_list = list()
        if vehicles.val() is not None:
            for vehicle in vehicles.each():
                vehicles_list.append(vehicle.val())
        context = {'app': app, 'title': 'Display Vehicles'}
        context.update(get_user_details(self, context))
        paginator = Paginator(vehicles_list, settings.VEHICLE_COUNT)
        page = self.request.GET.get('page')
        vehicles = paginator.get_page(page)
        context.update({'vehicles': vehicles})
        return context


# template - vehicle_display.html
class DisplayVehicleDetail(TemplateView):
    template_name = 'manufacturer/vehicle_display.html'

    def get_context_data(self, **kwargs):
        user = self.request.session['user']
        context = {'app': app, 'title': 'Display Vehicles'}
        context.update(get_user_details(self, context))
        chassis_no = kwargs['pk']
        vehicle = database.child('manufacturer').child(str(user['userId'])).child('vehicles').child(
            str(chassis_no)).get()
        if vehicle.val() is not None:
            context.update({'vehicle': vehicle.val()})
        return context


# template - assign_dealer.html
class AssignDealer(TemplateView):
    template_name = 'manufacturer/assign_dealer.html'
    
    def get(self, request, *args, **kwargs):
        form = DealerAssignForm()
        context = {'app': app, 'title': 'Assign Dealers', 'form': form}
        context.update(get_user_details(self, context))
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = DealerAssignForm(request.POST)
        context = {'app': app, 'title': 'Assign Dealers'}
        context.update(get_user_details(self, context))
        if form.is_valid():
            # try:
                dealer_name = request.POST.get('select_dealer')
                # print(dealer_name)
                chassis_alloted = request.POST.get('chassis_alloted')
                # print(chassis_alloted)
                if str(chassis_alloted).find(',') != -1 and str(chassis_alloted).find('-') != -1:
                    # Range as well as comma seperated
                    chassis_list = str(chassis_alloted).split(',')
                    # print(chassis_list)
                    for chassis in chassis_list:
                        if str(chassis).find('-') != -1:
                            chassis_list.remove(chassis)
                            for i in get_range(chassis):
                                chassis_list.append(i)
                    # print(chassis_list)
                elif str(chassis_alloted).find(',') != -1:
                    # Comma Seperated
                    chassis_list = str(chassis_alloted).split(',')
                elif str(chassis_alloted).find('-') != -1:
                    # Range
                    chassis_list = get_range(chassis_alloted)
                elif len(str(chassis_alloted)) == 12:
                    # Single Chassis
                    chassis_list = [chassis_alloted]
                else:
                    # Invalid Chassis
                    messages.error(request, f'Chassis Alloted Field is not valid')
                # print(chassis_list)
                # Remove Wrong Chassis No
                for chassis in chassis_list:
                    if (len(chassis)) != 12:
                        chassis_list.remove(chassis)
                # print(chassis_list)
                # Remove Duplicates
                chassis_list = remove_duplicates_from_list(chassis_list)
                # print(chassis_list)
                chassis_list.sort()
                # print(chassis_list)
                dealer_id = get_dealer_id(dealer_name)
                # print(dealer_id)
                # manufacturer id
                
                user = request.session['user']
                today = datetime.now()
                print(today.strftime('%d/%m/%Y %H:%M:%S'))
                date_time = today.strftime('%d/%m/%Y %H:%M:%S')
                database.child('requests').child('chassis_alloted').child(str(dealer_id)).child(str(user['userId'])).child('chassis_list').update(chassis_list)
                database.child('requests').child('chassis_alloted').child(str(dealer_id)).child(str(user['userId'])).child('date_time').set(date_time)
                database.child('requests').child('chassis_alloted').child(str(dealer_id)).child(str(user['userId'])).child('manufacturer_name').set(context.get('company_name'))
                # print(database.child('requests').child(
                #     'chassis_alloted').child(str(dealer_id)).get().val())
                # print('done')
                form = DealerAssignForm()
                messages.success(request, f'Successfully Assigned')
            # except:
            #     messages.error(request, f'System Error or Wrong Input')
        else:
            messages.error(request, f'Enter Valid Data')
        context.update({'form': form})
        return render(request, self.template_name, context)


class UpdateView(TemplateView):
    template_name = 'manufacturer/update.html'

    def get_context_data(self, **kwargs):
        context = {'app': app, 'title': 'Update Vehicle'}
        context.update(get_user_details(self, context))
        return context

    def get(self, request, *args, **kwargs):
        user = self.request.session['user']
        form = None
        try:
            chassis_no = kwargs['pk']
            vehicle = database.child('manufacturer').child(str(user['userId'])).child('vehicles').child(
                str(chassis_no)).get()
            vehicle = dict(OrderedDict(vehicle.val()))
            # print(vehicle)
            form = AddVehicleForm(initial=vehicle)
        except:
            messages.error(request, f'Vehicle Not Available')
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AddVehicleForm(request.POST)
        if form.is_valid():
            try:
                vehicle = form.save(commit=False)
                vehicle = vehicle.__dict__
                for key in ['_state', 'id']:
                    vehicle.pop(key)
                user = get_user(request)
                database.child('manufacturer').child(str(user['userId'])).child('vehicles').child(
                    vehicle.get('chassis_no')).set(vehicle)
                messages.success(request, f'Updated Successfully')
            except:
                messages.error(request, f'Error Occured')
        else:
            messages.error(request, f'Details are Invalid')
        return render(request, self.template_name, {'form': form})


class DeleteView(TemplateView):
    template_name = 'manufacturer/delete.html'

    def get(self, request, *args, **kwargs):
        try:
            chassis = kwargs['pk']
            # print(chassis)
            user = get_user(request)
            database.child('manufacturer').child(str(user['userId'])).child('vehicles').child(str(chassis)).remove()
        except:
            messages.error(request, f'Deletion Failed')
        return redirect('manufacturer-display-manufactured')
