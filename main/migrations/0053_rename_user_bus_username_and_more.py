# Generated by Django 4.1.4 on 2022-12-24 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0052_alter_bus_user_alter_postdestinations_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bus',
            old_name='user',
            new_name='userName',
        ),
        migrations.RenameField(
            model_name='postdestinations',
            old_name='user',
            new_name='userName',
        ),
    ]
