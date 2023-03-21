# Generated by Django 4.1 on 2022-12-06 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='monthlySales',
            fields=[
                ('sale_id', models.AutoField(db_column='sale_id', primary_key=True, serialize=False)),
                ('daily_sale', models.IntegerField(blank=True, db_column='daily_sale', null=True)),
            ],
            options={
                'db_table': 'monthly sale',
            },
        ),
        migrations.DeleteModel(
            name='test',
        ),
    ]
