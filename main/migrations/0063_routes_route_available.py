# Generated by Django 4.1.4 on 2023-01-07 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0062_busbookingdetails_booked_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='routes',
            name='route_available',
            field=models.DateField(blank=True, db_column='booked_date', null=True),
        ),
    ]
