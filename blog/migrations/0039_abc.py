# Generated by Django 4.0.3 on 2022-04-08 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0038_vehiclepayments'),
    ]

    operations = [
        migrations.CreateModel(
            name='abc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a', models.CharField(max_length=20)),
                ('b', models.CharField(max_length=20)),
            ],
        ),
    ]
