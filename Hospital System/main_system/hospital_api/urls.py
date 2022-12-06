from django.urls import path

from . import personaldataview
from . import vitalsignsview

urlpatterns = [
    path('personal/', personaldataview.index, name='personal.index'),
    path('personal/get/', personaldataview.get, name='personal.get'),
    path('personal/add/', personaldataview.add, name='personal.add'),

    path('vitalsigns/', vitalsignsview.index, name='vitalsign.index'),
    path('vitalsigns/get/', vitalsignsview.get, name='vitalsign.get'),
    path('vitalsigns/add/', vitalsignsview.add, name='vitalsign.add'),
]