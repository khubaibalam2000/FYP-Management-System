from django.db import models


class PersonalInfo(models.Model):
    id = models.IntegerField(blank=True, null=False, primary_key=True)
    name = models.TextField(blank=True, null=True)
    dob = models.TextField(db_column='DOB', blank=True, null=True)  # Field name made lowercase.
    city = models.TextField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    ssn = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personal_info'

class VitalSigns(models.Model):
    id = models.IntegerField(blank=True, null=False, primary_key=True)
    heart_rate = models.TextField(db_column='Heart_Rate', blank=True, null=True)  # Field name made lowercase.
    blood_pressure = models.TextField(db_column='Blood_Pressure', blank=True, null=True)  # Field name made lowercase.
    respiration_rate = models.TextField(db_column='Respiration_Rate', blank=True, null=True)  # Field name made lowercase.
    oxygen_saturation = models.TextField(db_column='Oxygen_Saturation', blank=True, null=True)  # Field name made lowercase.
    temperature = models.TextField(db_column='Temperature', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vital_signs'