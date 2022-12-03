from rest_framework import serializers
from . import models

class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.Diagnosis
        fields = '__all__'