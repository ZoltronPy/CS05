# Generated by Django 5.1.4 on 2024-12-08 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0025_alter_hotel_city_alter_hotel_stars'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travelinfo',
            name='destination_hotels',
        ),
        migrations.AddField(
            model_name='travelinfo',
            name='Hotel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='hotels', to='viewer.hotel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='travelinfo',
            name='city',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='city_travel_info', to='viewer.city'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='travelinfo',
            name='tour_name',
            field=models.CharField(default='Tour name ', max_length=32, unique=True),
        ),
    ]
