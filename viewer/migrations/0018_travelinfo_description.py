# Generated by Django 5.1.4 on 2024-12-07 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0017_alter_tourpurchase_adult_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelinfo',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
