from django.db import models


class VehicleData(models.Model):
    owner_name = models.CharField(max_length=50)
    registration_no = models.CharField(max_length=11)
    chassis_no = models.CharField(max_length=17)
    engine_no = models.CharField(max_length=10)
    fitness_validity = models.CharField(max_length=11)
    fuel_type = models.CharField(max_length=10)
    insurance_deadline = models.CharField(max_length=11)
    maker = models.TextField()
    model = models.TextField()
    rc_status = models.CharField(max_length=10)
    registration_authority = models.CharField(max_length=50)
    vehicle_class = models.TextField()
