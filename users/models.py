from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    contact = models.CharField(max_length=13)
    industry_license = models.FileField(upload_to='manufacturer/profile/')
