# Generated by Django 4.1 on 2022-12-06 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0002_monthlysales_delete_test'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='monthlysales',
            table='monthly_sale',
        ),
    ]
