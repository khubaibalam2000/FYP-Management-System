from django.urls import path

from . import view

urlpatterns = [
    path('', view.index, name='diagnosis.index'),
    path('get/', view.get, name='diagnosis.get'),
    path('add/', view.add, name='diagnosis.add'),
]