# Generated by Django 2.2.5 on 2019-09-25 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturer', '0012_auto_20190924_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturer',
            name='license_no',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
