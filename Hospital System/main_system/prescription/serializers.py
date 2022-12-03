from rest_framework import serializers
from . import models

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.Prescription
        fields = '__all__'