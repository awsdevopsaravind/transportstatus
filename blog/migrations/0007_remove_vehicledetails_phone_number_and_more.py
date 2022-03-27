# Generated by Django 4.0.3 on 2022-03-22 21:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_vehicledetails_tripdetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicledetails',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='vehicledetails',
            name='phonenumber',
            field=models.CharField(default=12345, max_length=16, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')]),
            preserve_default=False,
        ),
    ]