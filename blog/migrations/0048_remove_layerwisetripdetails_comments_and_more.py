# Generated by Django 4.0.3 on 2022-04-25 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0047_layerwisetripdetails_approved_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='layerwisetripdetails',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='layerwisetripdetails',
            name='royalty_image_back',
        ),
        migrations.RemoveField(
            model_name='layerwisetripdetails',
            name='verifiedbyengineer',
        ),
        migrations.RemoveField(
            model_name='layerwisetripdetails',
            name='verifiedbymalli',
        ),
        migrations.RemoveField(
            model_name='layerwisetripdetails',
            name='verifiedbysuresh',
        ),
        migrations.AlterField(
            model_name='layerwisetripdetails',
            name='approved',
            field=models.CharField(blank=True, default='Deny', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='layerwisetripdetails',
            name='forwarded',
            field=models.CharField(blank=True, default='Deny', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='layerwisetripdetails',
            name='verified',
            field=models.CharField(blank=True, default='Deny', max_length=200, null=True),
        ),
    ]
