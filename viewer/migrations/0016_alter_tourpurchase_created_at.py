# Generated by Django 5.1.4 on 2024-12-07 12:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0015_alter_tourpurchase_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourpurchase',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created at'),
        ),
    ]
