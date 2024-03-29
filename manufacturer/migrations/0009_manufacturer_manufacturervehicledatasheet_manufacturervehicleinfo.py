# Generated by Django 2.2.5 on 2019-09-24 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('manufacturer', '0008_auto_20190917_1906'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50)),
                ('owner_name', models.CharField(max_length=50)),
                ('company_email', models.EmailField(max_length=254)),
                ('company_contact', models.CharField(max_length=13)),
                ('company_license', models.FileField(upload_to='manufacturer/profile/')),
            ],
        ),
        migrations.CreateModel(
            name='ManufacturerVehicleDataSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='datasheets/')),
            ],
        ),
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
                ('price', models.CharField(default=0, max_length=15)),
                ('status', models.CharField(default='Not Registered', max_length=20)),
            ],
        ),
    ]
