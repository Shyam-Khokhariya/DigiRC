from django.db import models


class Buyer(models.Model):
    name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    husband_name = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=10)
    age = models.CharField(max_length=2)
    address1 = models.TextField()
    address2 = models.TextField()
    birth_place = models.CharField(max_length=20)
    email = models.EmailField()
    contact1 = models.CharField(max_length=13)
    contact2 = models.CharField(max_length=13, null=True)
    license_no = models.CharField(max_length=20)
    profile_pic = models.FileField(upload_to='buyer/profile/')
    driving_license = models.FileField(upload_to='buyer/license/')
