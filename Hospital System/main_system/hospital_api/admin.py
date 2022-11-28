from django.contrib import admin
from .models import PersonalInfo, VitalSigns

admin.site.register(PersonalInfo)
admin.site.register(VitalSigns)