# Generated by Django 4.2 on 2023-04-15 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_alter_medical_treatment_advice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='blood_group',
            field=models.CharField(choices=[('empty', ''), ('Group A', 'Group A'), ('Group B', 'Group B'), ('Group AB', 'Group AB'), ('Group O', 'Group O')], default='empty', max_length=10),
        ),
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('empty', ''), ('Male', 'Male'), ('Female', 'Female')], default='empty', max_length=10),
        ),
    ]
