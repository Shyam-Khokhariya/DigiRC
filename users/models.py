from django.db import models


class UserData(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    is_admin_user = models.BooleanField(default=False)
