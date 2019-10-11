import random
import _csv
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import AddVehicleForm, AddVehicleFileForm
from users.user_statistics import *

app = settings.APP_NAME

from django.shortcuts import render
from .fusioncharts import FusionCharts
import pandas as pd
from collections import OrderedDict
import numpy as np

color=['#B22222','#DC143C','#FF0000','#FF6347','#FF7F50','#CD5C5C','#F08080','#E9967A','#FA8072','#FFA07A',
'#FF4500','#FF8C00','#FFA500','#FFD700','#B8860B','#DAA520','#EEE8AA','#BDB76B','#F0E68C','#808000','#FFFF00','#9ACD32','#556B2F',
'#6B8E23','#7CFC00','#7FFF00','#ADFF2F','#006400','#008000','#228B22','#00FF00','#32CD32','#90EE90','#98FB98','#8FBC8F','#00FA9A',
'#00FF7F','#2E8B57','#66CDAA','#3CB371','#20B2AA','#2F4F4F','#008080','#008B8B','#00FFFF','#00FFFF','#E0FFFF','#00CED1','#40E0D0',
'#48D1CC','#AFEEEE','#7FFFD4','#B0E0E6','#5F9EA0','#4682B4','#6495ED','#00BFFF','#1E90FF','#ADD8E6','#87CEEB','#87CEFA','#191970',
'#000080','#00008B','#0000CD','#0000FF','#4169E1','#8A2BE2','#4B0082','#483D8B','#6A5ACD','#7B68EE','#9370DB','#8B008B','#9400D3',
'#9932CC','#BA55D3','#800080','#D8BFD8','#DDA0DD','#EE82EE','#FF00FF','#DA70D6','#C71585','#DB7093','#FF1493','#FF69B4','#FFB6C1',
'#FFC0CB','#FAEBD7','#F5F5DC','#FFE4C4','#FFEBCD','#F5DEB3','#FFF8DC','#FFFACD','#FAFAD2','#FFFFE0','#8B4513','#A0522D','#D2691E',
'#CD853F','#F4A460','#DEB887','#D2B48C','#BC8F8F','#FFE4B5','#FFDEAD','#FFDAB9','#FFE4E1','#FFF0F5','#FAF0E6','#FDF5E6','#FFEFD5',
'#FFF5EE','#F5FFFA','#708090','#778899','#B0C4DE','#E6E6FA','#FFFAF0','#F0F8FF','#F8F8FF','#F0FFF0','#FFFFF0','#F0FFFF','#FFFAFA',
'#000000','#696969','#808080','#A9A9A9','#C0C0C0','#D3D3D3','#DCDCDC','#F5F5F5','#FFFFFF','#800000','#8B0000','#A52A2A']
def chart1(vehicles, context):
    dataSource = {}
    data = pd.DataFrame()
    for v in vehicles.each():
        # print(v.val())
        data = data.append(pd.DataFrame([v.val()]))
    # print(data.columns)
    context['data1'] = data
    # print(context['data1'])
    chartData = {}
    u_body_type= data.vehicle_type.unique()
    list_body_type = list(data.vehicle_type)
    # print(u_body_type)
    for d in u_body_type:
        chartData[d] = list_body_type.count(d)
    # color_count=len(u_body_type)
    # red=random.sample(range(0,255),color_count)
    # green=random.sample(range(0,255),color_count)
    # blue=random.sample(range(0,255),color_count)
    # # p = lambda: random.randint(0, 255)
    # color = '#%02X%02X%02X' % (red[0], green[0], blue[0])
    # # print(color_count)
    # for i in range(1,color_count):
    #     # r = lambda: random.randint(0, 255)
    #     color=color+(',#%02X%02X%02X' % (red[i], green[i], blue[i]))
    chartConfig = {
        "borderColor": "#ffffff",
        "bgColor": "#ffffff",
        "borderAlpha": "80",
        "theme": "fusion",
        "xAxisName": "Vehicle Type",
        "yAxisName": "Sales",
        "palettecolors": color,

        "showRealTimeValue": "0",

    }

    # The `chartData` dict contains key-value pairs data
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
    # print(total_vehicle1["categories"][0]["category"])
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
    print(color)
    # print(data.status.unique())

    chartConfig = {
        "defaultCenterLabel": "Vehicle Manufactured: "+str(data.shape[0]),
        # "centerLabel": " $label : $value",
        "pieRadius": "60%",
        "doughnutRadius": "158%",
        "showLegend":'1',
        "use3DLighting":'1',
        "palettecolors": color,
        "showLabels":'0',
        "showToolTip":'1',
        "showToolBarButtonToolText":'0',
        "enableSmartLabels": "0",
        "manageLabelOverflow": "0",
        "showPercentInToolTip": "0",
        "useEllipsesWhenOverflow": "0",
        "theme": "fusion"
    }


    # The `chartData` dict contains key-value pairs data
    chartData = {}
    u_body_type = data.vehicle_type.unique()
    list_body_type = list(data.vehicle_type)
    # print(u_body_type)
    for d in u_body_type:
        chartData[d] = list_body_type.count(d)
    # print(chartData)
    dataSource["chart"] = chartConfig
    dataSource["data"] = []

    for label, value in chartData.items():
        data1 = {}
        data1["label"] = label
        data1["value"] = value
        dataSource["data"].append(data1)

    Dough = FusionCharts("doughnut2d", "do", "100%", "600%", "dough", "json", dataSource)
    context['op_dough'] = Dough.render()


class Dashboard(TemplateView):
    template_name = 'manufacturer/home.html'

    def get_context_data(self, **kwargs):
        user = get_user(self.request)
        vehicles = database.child('manufacturer').child(str(user['userId'])).child('vehicles').get()
        context = {'app': app, 'title': 'Dashboard'}
        if vehicles.each()!=None:
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
                    print(path)
                    fields = list()
                    rows = list()
                    print(path)
                    with open(path, 'r') as csvfile:
                        print('hello')
                        csvreader = _csv.reader(csvfile)
                        for row in csvreader:
                            print(row)
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
                        database.child('manufacturer').child(str(user['userId'])).child('vehicles').child(
                            vehicle.get('chassis_no')).set(vehicle)
                    print('done')
                    os.remove(path)
                    messages.success(request, f'Saved Successfully')
                else:
                    messages.error(request, f'Datasheet is not in proper format')
            else:
                messages.error(request, f'Invalid File')
        context = {'app': app, 'title': 'Add Vehicle', 'form1': form1, 'form2': form2}
        context.update(get_user_details(self, context))
        return render(request, self.template_name, context)


def add_vehicle(request):
    form1 = AddVehicleForm()
    form2 = AddVehicleFileForm()
    if request.method == 'POST':
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
                    try:
                        form2.save()
                        file_name = get_file_name(request, 'file')
                        path = os.path.join(settings.BASE_DIR, 'media') + '/datasheets/' + file_name
                        fields = list()
                        rows = list()
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
                        user = get_user(request)
                        for vehicle in data_list:
                            database.child('manufacturer').child(str(user['userId'])).child('vehicles').child(
                                vehicle.get('chassis_no')).set(vehicle)
                        os.remove(path)
                        messages.success(request, f'Saved Successfully')
                    except:
                        messages.error(request, f'Error Occured')
                else:
                    messages.error(request, f'Datasheet is not in proper format')
            else:
                messages.error('Invalid File')
    context = {'app': app, 'title': 'Add Vehicle', 'form1': form1, 'form2': form2}
    context.update(get_user_details(request, context))
    return render(request, 'manufacturer/add.html', context)


class DisplayManufactured(TemplateView):
    template_name = 'manufacturer/manufactured_display.html'

    def get_context_data(self, **kwargs):
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
        print(vehicles)
        context.update({'vehicles': vehicles})
        return context


class DisplayVehicleDetail(TemplateView):
    template_name = 'manufacturer/vehicle_display.html'

    def get_context_data(self, **kwargs):
        user = self.request.session['user']
        vehicles = database.child('manufacturer').child(str(user['userId'])).child('vehicles').get()
        context = {'app': app, 'title': 'Display Vehicles'}
        context.update(get_user_details(self, context))
        if vehicles.val() is not None:
            for vehicle in vehicles.each():
                if str(self.request.path).endswith(vehicle.key()):
                    context.update({'vehicle': vehicle.val()})
                    break
        return context
