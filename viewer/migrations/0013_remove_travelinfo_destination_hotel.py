# Generated by Django 5.1.4 on 2024-12-07 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0012_alter_continent_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travelinfo',
            name='destination_hotel',
        ),
    ]
