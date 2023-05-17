# Generated by Django 4.1 on 2022-12-07 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0004_alter_monthlysales_sale_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='month_sale',
            fields=[
                ('sale_id', models.DateField(db_column='sale_id', primary_key=True, serialize=False)),
                ('month_sale', models.IntegerField(blank=True, db_column='daily_sale', null=True)),
            ],
            options={
                'db_table': 'month_sale',
            },
        ),
    ]