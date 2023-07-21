# Generated by Django 4.2 on 2023-07-21 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20)),
            ],
        ),
        migrations.RenameField(
            model_name='platenumber',
            old_name='plate_number',
            new_name='number',
        ),
    ]
