from rest_framework import serializers
from . import models

class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.PersonalInfo
        fields = '__all__'

class VitalSignsSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.VitalSigns
        fields = '__all__'
