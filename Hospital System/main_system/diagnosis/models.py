from django.db import models

class Diagnosis(models.Model):
    diagnose = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diagnosis'
        app_label  = 'diagnosis_data'
