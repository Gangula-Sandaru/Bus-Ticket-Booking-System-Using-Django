# Generated by Django 4.1 on 2022-12-06 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0043_busticket_ticket_counted'),
    ]

    operations = [
        migrations.AddField(
            model_name='busticket',
            name='ticket_qr_code',
            field=models.ImageField(blank=True, db_column='qr_code', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='busticket',
            name='ticket_counted',
            field=models.BooleanField(blank=True, db_column='ticket_count', default=0, null=True),
        ),
    ]
