# Generated by Django 2.2.5 on 2019-09-24 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0008_auto_20190923_2119'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Manufacturer',
        ),
        migrations.DeleteModel(
            name='ManufacturerVehicleDataSheet',
        ),
        migrations.DeleteModel(
            name='ManufacturerVehicleInfo',
        ),
    ]