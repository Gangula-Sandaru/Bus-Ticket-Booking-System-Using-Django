# Generated by Django 4.1 on 2022-11-24 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_rename_f_name_givefeedback_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubEmail',
            fields=[
                ('sub_id', models.AutoField(db_column='sub_id', primary_key=True, serialize=False)),
                ('email_name', models.EmailField(db_column='email_address', max_length=254)),
            ],
            options={
                'db_table': 'email_subscription',
            },
        ),
    ]
