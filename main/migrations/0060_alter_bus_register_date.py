# Generated by Django 4.1.4 on 2022-12-29 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0059_bus_register_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='register_date',
            field=models.DateTimeField(auto_now_add=True, db_column='registerdate', null=True),
        ),
    ]
