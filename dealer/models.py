from django.db import models


class Dealer(models.Model):
    shop_name = models.CharField(max_length=50)
    owner_name = models.CharField(max_length=50)
    shop_email = models.EmailField()
    shop_contact = models.CharField(max_length=13)
    owner_contact = models.CharField(max_length=13)
    license_no = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    shop_logo = models.FileField(upload_to='dealer/logo/')
    shop_license = models.FileField(upload_to='dealer/license/')
