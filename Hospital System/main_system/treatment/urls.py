from django.urls import path

from . import view

urlpatterns = [
    path('', view.index, name='treatment.index'),
    path('get/', view.get, name='treatment.get'),
    path('add/', view.add, name='treatment.add'),
    path('deletetreatment/', view.deleteDataTreatment, name='diagnosis.deleteDataTreatment'),
]