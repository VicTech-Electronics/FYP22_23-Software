# Generated by Django 4.1.4 on 2023-03-02 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('heat_rate', models.FloatField()),
                ('body_temp', models.FloatField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.device')),
            ],
        ),
    ]
