# Generated by Django 4.1.4 on 2023-03-02 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_rename_heat_rate_request_heart_rate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request',
            old_name='body_temp',
            new_name='body_temperature',
        ),
    ]
