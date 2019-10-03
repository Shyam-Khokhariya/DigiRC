# Generated by Django 2.2.5 on 2019-09-30 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='profile_pic',
            field=models.FileField(default=1, upload_to='buyer/profile/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='buyer',
            name='driving_license',
            field=models.FileField(upload_to='buyer/license/'),
        ),
    ]