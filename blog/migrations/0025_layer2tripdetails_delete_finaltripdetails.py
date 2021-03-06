# Generated by Django 4.0.3 on 2022-04-02 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_finaltripdetails_initialtripdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='Layer2TripDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_date', models.DateField()),
                ('tf_number', models.CharField(max_length=200)),
                ('qty_m3', models.FloatField()),
                ('royalty_image_front', models.ImageField(upload_to='')),
                ('royalty_image_back', models.ImageField(blank=True, upload_to='')),
                ('qty_ton', models.FloatField()),
                ('waybill_image_front', models.ImageField(upload_to='')),
                ('waybill_image_back', models.ImageField(blank=True, upload_to='')),
                ('sendtomalli', models.PositiveSmallIntegerField(choices=[(1, 'Confirm Send'), (2, 'No, require more time')], default=1)),
                ('company_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.companyname')),
                ('driver_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.transporterdetails')),
                ('load_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.loadtype')),
                ('quarry_owner_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.quarrydetails')),
                ('vehicle_number', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.vehicledetails')),
            ],
        ),
        migrations.DeleteModel(
            name='FinalTripDetails',
        ),
    ]
