# Generated by Django 4.1 on 2022-12-01 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_routes_vehicle_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='routes',
            old_name='vehicle_status',
            new_name='route_status',
        ),
    ]
