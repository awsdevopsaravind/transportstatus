# Generated by Django 4.0.3 on 2022-03-22 21:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_remove_vehicledetails_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicledetails',
            name='phonenumber',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')]),
        ),
    ]