# Generated by Django 4.0.3 on 2022-04-09 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0040_exceldata1'),
    ]

    operations = [
        migrations.DeleteModel(
            name='abc',
        ),
        migrations.AddField(
            model_name='vehiclepayments',
            name='amount_receipt',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='vehiclepayments',
            name='vehicle_owner_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.transporterdetails'),
        ),
        migrations.AlterField(
            model_name='vehiclepayments',
            name='vehicle_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.vehicledetails'),
        ),
    ]
