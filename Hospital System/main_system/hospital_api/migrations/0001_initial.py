# Generated by Django 4.1.3 on 2022-11-28 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalInfo',
            fields=[
                ('id', models.IntegerField(blank=True, primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('dob', models.TextField(blank=True, db_column='DOB', null=True)),
                ('city', models.TextField(blank=True, null=True)),
                ('province', models.TextField(blank=True, null=True)),
                ('gender', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
                ('phone', models.TextField(blank=True, null=True)),
                ('ssn', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'personal_info',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VitalSigns',
            fields=[
                ('id', models.IntegerField(blank=True, primary_key=True, serialize=False)),
                ('heart_rate', models.TextField(blank=True, db_column='Heart_Rate', null=True)),
                ('blood_pressure', models.TextField(blank=True, db_column='Blood_Pressure', null=True)),
                ('respiration_rate', models.TextField(blank=True, db_column='Respiration_Rate', null=True)),
                ('oxygen_saturation', models.TextField(blank=True, db_column='Oxygen_Saturation', null=True)),
                ('temperature', models.TextField(blank=True, db_column='Temperature', null=True)),
            ],
            options={
                'db_table': 'vital_signs',
                'managed': False,
            },
        ),
    ]
