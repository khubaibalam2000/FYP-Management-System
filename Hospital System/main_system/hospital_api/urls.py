from django.urls import path

from . import personaldataview
from . import vitalsignsview

urlpatterns = [
    path('personal/', personaldataview.index, name='personal.index'),
    path('personal/get/', personaldataview.get, name='personal.get'),
    path('personal/add/', personaldataview.add, name='personal.add'),
    path('personal/requestForData/', personaldataview.requestForData, name='personal.requestForData'),
    path('personal/inform/', personaldataview.inform, name='personal.inform'),
    path('personal/epdgwithconnection/', personaldataview.generateExternalPDGWithConnections, name='personal.generateExternalPDGWithConnections'),
    path('personal/epdgwithoutconnection/', personaldataview.generateExternalPDGWithoutConnections, name='personal.generateExternalPDGWithoutConnections'),
    path('personal/ipdg/', personaldataview.internalPDG, name='personal.internalPDG'),
    path('personal/eXdataReport/', personaldataview.eXdataReport, name='personal.eXdataReport'),
    path('personal/eHdataReport/', personaldataview.eHdataReport, name='personal.eHdataReport'),
    path('personal/ireport/', personaldataview.iReport, name='personal.iReport'),
    path('personal/databreach/', personaldataview.dataBreachReport, name='personal.dataBreachReport'),
    path('personal/policies/', personaldataview.storePoliciesOnMultiChain, name='personal.storePoliciesOnMultiChain'),
    path('personal/checkpolicy/', personaldataview.checkPoliciesOnMultiChain, name='personal.checkPoliciesOnMultiChain'),
    path('personal/deletehospitaldata/', personaldataview.deleteHospitalData, name='personal.deleteHospitalData'),

    path('vitalsigns/', vitalsignsview.index, name='vitalsign.index'),
    path('vitalsigns/get/', vitalsignsview.get, name='vitalsign.get'),
    path('vitalsigns/add/', vitalsignsview.add, name='vitalsign.add'),
]