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


# class VehicleRegFormData(models.Model):
#     rto_name = models.CharField(max_length=50)
#     dealer_name = models.CharField(max_length=50)
#
#     owner_type = models.CharField(max_length=50)
#     owner_name = models.CharField(max_length=50)
#     father_name = models.CharField(max_length=50)
#     mobile_number = models.CharField(max_length=50)
#     email = models.CharField(max_length=50)
#     pan = models.CharField(max_length=50)
#
#     address1 = models.TextField()
#     city1 = models.CharField(max_length=50)
#     pincode1 = models.CharField(max_length=6)
#
#     address2 = models.TextField(null=True)
#     city2 = models.CharField(max_length=50, null=True)
#     pincode2 = models.CharField(max_length=6, null=True)
#
#     registration_type = models.CharField(max_length=50)
#     vehicle_class = models.CharField(max_length=50)
#     vehicle_type = models.CharField(max_length=50)
#     vehicle_make = models.CharField(max_length=50)
#     vehicle_model = models.CharField(max_length=50)
#
#     manufacturing_date = models.CharField(max_length=50)
#     sale_date = models.CharField(max_length=50)
#     sale_amount = models.CharField(max_length=50)
#     engine_no = models.CharField(max_length=50)
#     chassis_no = models.CharField(max_length=50)
#     color = models.CharField(max_length=50)
#     lazer_code = models.CharField(max_length=50)
#
#     tax_mode = models.CharField(max_length=50)
#     insurance_company = models.CharField(max_length=50, null=True)
#     insurance_type = models.CharField(max_length=50, null=True)
#     insurance_from = models.CharField(max_length=50, null=True)
#     insurance_to = models.CharField(max_length=50, null=True)
#     covernote_no = models.CharField(max_length=50, null=True)
#
#     hypothecation = models.CharField(max_length=50, null=True)
#
#     sale_certificate = models.ImageField()
#     road_worthiness_certificate = models.ImageField()
#     identity_proof = models.ImageField()
#     insurance_certificate = models.ImageField(null=True)
#     address_proof = models.ImageField()
#     bill_of_entry_submitted_to_custom = models.ImageField(null=True)
#     body_builder_certificate = models.ImageField(null=True)
