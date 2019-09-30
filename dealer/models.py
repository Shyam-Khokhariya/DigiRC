from django.db import models


class Dealer(models.Model):
    shop_name = models.CharField(max_length=50)
    owner_name = models.CharField(max_length=50)
    shop_email = models.EmailField()
    shop_contact = models.CharField(max_length=13)
    owner_contact = models.CharField(max_length=13)
    shop_logo = models.FileField(upload_to='dealer/logo/')
    shop_license = models.FileField(upload_to='dealer/license/')
