# Generated by Django 2.2.4 on 2019-09-13 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManufacturerVehicleInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chassis_no', models.CharField(max_length=17)),
                ('engine_no', models.CharField(max_length=10)),
                ('fuel_type', models.TextField()),
                ('maker', models.TextField()),
                ('model', models.TextField()),
                ('vehicle_class', models.TextField()),
                ('body_type', models.TextField()),
                ('vehicle_type', models.TextField()),
                ('manufacture_month', models.CharField(max_length=3)),
                ('manufacture_year', models.CharField(max_length=4)),
                ('number_of_cylinders', models.CharField(max_length=2)),
                ('horse_power', models.CharField(max_length=4)),
                ('cubic_capacity', models.CharField(max_length=4)),
                ('wheel_base', models.CharField(max_length=5)),
                ('seating_capacity', models.CharField(max_length=4)),
                ('unladen_weight', models.CharField(max_length=10)),
                ('color', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='VehicleData',
        ),
    ]
