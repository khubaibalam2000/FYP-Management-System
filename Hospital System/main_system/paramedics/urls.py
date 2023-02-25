from django.urls import path
from . import views

urlpatterns = [
    path('requestMOHForData/', views.requestMOHForData, name='moh.requestMOHForData'),
    path('deleteparadata/', views.deleteParamedicsData, name='moh.deleteParamedicsData'),
]