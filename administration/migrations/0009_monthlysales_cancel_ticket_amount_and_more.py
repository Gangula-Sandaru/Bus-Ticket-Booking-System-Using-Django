# Generated by Django 4.1.4 on 2022-12-15 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0008_delete_year_sale_alter_monthlysales_daily_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlysales',
            name='cancel_ticket_amount',
            field=models.DecimalField(blank=True, db_column='cancel_ticket_amount', decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='monthlysales',
            name='cancel_ticket_qty',
            field=models.IntegerField(blank=True, db_column='cancel_ticket_qty', null=True),
        ),
        migrations.AddField(
            model_name='monthlysales',
            name='pending_ticket_amount',
            field=models.DecimalField(blank=True, db_column='pending_ticket_amount', decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='monthlysales',
            name='pending_ticket_qty',
            field=models.IntegerField(blank=True, db_column='pending_ticket_qty', null=True),
        ),
        migrations.AddField(
            model_name='monthlysales',
            name='total_ticket_qty',
            field=models.IntegerField(blank=True, db_column='total_ticket_qty', null=True),
        ),
        migrations.AddField(
            model_name='monthlysales',
            name='used_ticket_amount',
            field=models.DecimalField(blank=True, db_column='used_ticket_amount', decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='monthlysales',
            name='used_ticket_qty',
            field=models.IntegerField(blank=True, db_column='used_ticket_qty', null=True),
        ),
    ]
