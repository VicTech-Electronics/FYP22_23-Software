# Generated by Django 4.1.4 on 2023-02-27 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_request_response_date_alter_request_response_time'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Device',
        ),
    ]
