from django.urls import path
from . import views

urlpatterns = [
    path('requestData/', views.requestData, name='moh.requestData'),
    path('sendToParamedics/', views.sendToParamedics, name='moh.sendToParamedics'),
    path('automateddeletionmoh/', views.deleteDataBasedOnPolicyMOH, name='moh.deleteDataBasedOnPolicy'),
    path('deletemohdata/', views.deleteMOHData, name='moh.deleteMOHData'),
    path('updatepolicy/', views.updatePolicy, name='moh.updatePolicy'),
    path('pdgmoh/', views.generatePDGMOH, name='moh.generatePDGMOH'),
    path('expreqdatamoh/', views.experimentRequestData, name='moh.experimentRequestData'),
    path('callex/', views.callExperiments, name='moh.callExperiments'),
]