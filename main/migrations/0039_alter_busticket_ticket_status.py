# Generated by Django 4.1 on 2022-12-04 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_givefeedback_message_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busticket',
            name='ticket_status',
            field=models.IntegerField(db_column='ticket_status', default=0),
        ),
    ]
