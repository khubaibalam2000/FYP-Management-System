from django.db import models

class Prescription(models.Model):
    medicine = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medicines'
        app_label  = 'prescription_data'
