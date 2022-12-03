from django.db import models

class Treatment(models.Model):
    treatment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'treatments'
        app_label  = 'prescription_data'
