# Generated by Django 4.1 on 2022-11-26 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_alter_busdetails_total_distance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busdetails',
            name='total_distance',
            field=models.CharField(blank=True, db_column='totalDistance', max_length=5, null=True),
        ),
    ]