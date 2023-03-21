# Generated by Django 4.1 on 2022-12-07 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0007_rename_month_sale_year_sale'),
    ]

    operations = [
        migrations.DeleteModel(
            name='year_sale',
        ),
        migrations.AlterField(
            model_name='monthlysales',
            name='daily_sale',
            field=models.DecimalField(blank=True, db_column='daily_sale', decimal_places=2, max_digits=15, null=True),
        ),
    ]
