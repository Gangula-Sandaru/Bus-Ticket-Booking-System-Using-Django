# Generated by Django 4.1 on 2022-10-23 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_busseat_no_of_seat_remove_passenger_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passenger',
            name='select_bus',
            field=models.ManyToManyField(blank=True, null=True, to='main.bus'),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='userSearch_taxi',
            field=models.ManyToManyField(blank=True, null=True, to='main.taxi'),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='userSelectRoutes',
            field=models.ManyToManyField(blank=True, null=True, to='main.routes'),
        ),
    ]