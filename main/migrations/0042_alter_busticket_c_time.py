# Generated by Django 4.1 on 2022-12-05 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_busticket_ticket_expire_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busticket',
            name='c_time',
            field=models.DateTimeField(blank=True, db_column='c_time'),
        ),
    ]
