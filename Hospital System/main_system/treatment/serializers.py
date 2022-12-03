from rest_framework import serializers
from . import models

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.Treatment
        fields = '__all__'