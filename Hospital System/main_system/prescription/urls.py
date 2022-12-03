from django.urls import path

from . import view

urlpatterns = [
    path('', view.index, name='prescription.index'),
    path('get/', view.get, name='prescription.get'),
    path('add/', view.add, name='prescription.add'),
]