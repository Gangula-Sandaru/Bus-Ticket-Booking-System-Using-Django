# Generated by Django 4.1 on 2022-11-24 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_alter_postdestinations_table_givefeedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='givefeedback',
            old_name='f_name',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='givefeedback',
            old_name='l_name',
            new_name='last_name',
        ),
        migrations.RemoveField(
            model_name='givefeedback',
            name='owner_name',
        ),
    ]
