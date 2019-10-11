from django.db import models


class Buyer(models.Model):
    name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    husband_name = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=10)
    age = models.CharField(max_length=2)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    birth_place = models.CharField(max_length=20)
    email = models.EmailField()
    contact1 = models.CharField(max_length=13)
    contact2 = models.CharField(max_length=13, null=True)
    aadhar_no = models.CharField(max_length=12)
    license_no = models.CharField(max_length=20)
    profile_pic = models.FileField(upload_to='buyer/profile/')
    driving_license = models.FileField(upload_to='buyer/license/')
