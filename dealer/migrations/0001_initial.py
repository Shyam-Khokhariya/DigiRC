# Generated by Django 2.2.5 on 2019-09-25 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dealer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=50)),
                ('owner_name', models.CharField(max_length=50)),
                ('shop_email', models.EmailField(max_length=254)),
                ('shop_contact', models.CharField(max_length=13)),
                ('owner_contact', models.CharField(max_length=13)),
                ('shop_logo', models.FileField(upload_to='dealer/logo/')),
                ('shop_license', models.FileField(upload_to='dealer/license/')),
            ],
        ),
    ]