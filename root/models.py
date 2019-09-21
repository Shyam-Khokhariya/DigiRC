from django.db import models


class ManufacturerVehicleInfo(models.Model):
    chassis_no = models.CharField(max_length=17)
    engine_no = models.CharField(max_length=10)
    fuel_type = models.TextField()
    maker = models.TextField()
    model = models.TextField()
    vehicle_class = models.TextField()
    body_type = models.TextField()
    vehicle_type = models.TextField()
    manufacture_month = models.CharField(max_length=3)
    manufacture_year = models.CharField(max_length=4)
    number_of_cylinders = models.CharField(max_length=2)
    horse_power = models.CharField(max_length=4)
    cubic_capacity = models.CharField(max_length=4)     # CC of Vehicle
    wheel_base = models.CharField(max_length=5)     # distance between front and rear axles of vehicle in mm
    seating_capacity = models.CharField(max_length=4)
    unladen_weight = models.CharField(max_length=10)    # Weight of Vehicle when not loaded with goods
    color = models.TextField()
    price = models.CharField(max_length=15, default=0)
    status = models.CharField(max_length=20, default='Not Registered')


class ManufacturerVehicleDataSheet(models.Model):
    file = models.FileField(upload_to='datasheets/')


class Manufacturer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    contact = models.CharField(max_length=13)
    industry_license = models.FileField(upload_to='manufacturer/profile/')


class Feedback(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
