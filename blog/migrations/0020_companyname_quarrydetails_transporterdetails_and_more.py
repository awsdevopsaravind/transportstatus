# Generated by Django 4.0.3 on 2022-03-30 00:21

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_vehicledetails_driver_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='QuarryDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quarry_owner_name', models.CharField(max_length=100)),
                ('quarry_ton_rate', models.FloatField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransporterDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_owner_name', models.CharField(max_length=100)),
                ('owner_phone_number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')])),
            ],
        ),
        migrations.RenameField(
            model_name='tripdetails',
            old_name='loadtype',
            new_name='load_type',
        ),
        migrations.RenameField(
            model_name='vehicledetails',
            old_name='driver_phonenumber',
            new_name='driver_phone_number',
        ),
        migrations.RenameField(
            model_name='vehicledetails',
            old_name='phonenumber',
            new_name='phone_number',
        ),
        migrations.AlterField(
            model_name='tripdetails',
            name='royalty_image',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='tripdetails',
            name='waybill_image',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AddField(
            model_name='tripdetails',
            name='company_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.companyname'),
        ),
        migrations.AddField(
            model_name='tripdetails',
            name='quarry_owner_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.quarrydetails'),
        ),
    ]
