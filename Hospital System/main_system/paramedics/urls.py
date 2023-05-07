from django.urls import path
from . import views

urlpatterns = [
    path('requestMOHForData/', views.requestMOHForData, name='para.requestMOHForData'),
    path('deleteparadata/', views.deleteParamedicsData, name='para.deleteParamedicsData'),
    path('automateddeletionpara/', views.deleteDataBasedOnPolicyParamedics, name='para.deleteDataBasedOnPolicyParamedics'),
    path('updatepolicypara/', views.updatePolicyPara, name='para.updatePolicyPara'),
    path('pdgpara/', views.generatePDGPara, name='para.generatePDGPara'),
    path('expreqdatapm/', views.experimentRequestData, name='para.experimentRequestData'),
]