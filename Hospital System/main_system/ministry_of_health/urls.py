from django.urls import path
from . import views

urlpatterns = [
    path('requestData/', views.requestData, name='moh.requestData'),
    path('sendToParamedics/', views.sendToParamedics, name='moh.sendToParamedics'),
]