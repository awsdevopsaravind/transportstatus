# Generated by Django 4.0.3 on 2022-03-30 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_remove_vehicledetails_owner_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicledetails',
            name='owner_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.transporterdetails'),
        ),
    ]
