# Generated by Django 4.0.3 on 2022-04-03 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0029_alter_layerwisetripdetails_sendtomalli_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layerwisetripdetails',
            name='sendtomalli',
            field=models.IntegerField(default=0, max_length=1),
        ),
        migrations.AlterField(
            model_name='layerwisetripdetails',
            name='verifiedbymalli',
            field=models.IntegerField(default=0, max_length=1),
        ),
        migrations.AlterField(
            model_name='layerwisetripdetails',
            name='verifiedbysuresh',
            field=models.IntegerField(default=0, max_length=1),
        ),
    ]