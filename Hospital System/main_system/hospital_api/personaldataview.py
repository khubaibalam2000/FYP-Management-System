from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from .models import *
import sqlite3
from diagnosis.models import Diagnosis
from prescription.models import Prescription
from treatment.models import Treatment

def index(request):
    if request.method != "GET":
        return HttpResponse("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    persons = PersonalInfo.objects.all()
    serializer = PersonalInfoSerializer(persons, many=True)
    return JsonResponse(serializer.data, safe=False)

def get(request):
    if request.method != "GET":
        return HttpResponse("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    try:
        person = PersonalInfo.objects.get(id=request.GET['id'])
    except:
        return HttpResponse("Not Found", status=status.HTTP_404_NOT_FOUND)

    serializer = PersonalInfoSerializer(person)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET', 'POST'])
def add(request):
    serializer = PersonalInfoSerializer(data=request.data)
    if serializer.is_valid():
        if request.data != {}:
            serializer.save()
        return Response(serializer.data)
    else:
        return HttpResponse("Bad Data", status=status.HTTP_400_BAD_REQUEST)

def updateLinkingDatabase(queryOfLink, dbPath, toInsert):
    connection = sqlite3.connect(dbPath)
    cursor = connection.cursor()
    cursor.execute(queryOfLink, toInsert)
    connection.commit()
    connection.close()

def requestForData(request):
    if request.method != 'GET':
        return HttpResponse("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    hospitalPii = ['name', 'dob', 'city', 'province', 'gender', 'email', 'phone', 'ssn']
    hospitalVs = ['heart_rate', 'blood_pressure', 'respiration_rate', 'oxygen_saturation', 'temperature']
    diagnosis = ['diagnose']
    prescriptions = ['medicine']
    treatments = ['treatment']

    attributes = request.GET.getlist('attributes')
    froms = request.GET.getlist('froms')
    tos = request.GET.getlist('tos')
    ssn = request.GET['ssn']
    person = PersonalInfo.objects.filter(ssn=request.GET['ssn'])
    id = person.values_list('id')[0][0]

    vitalSigns = VitalSigns.objects.filter(id = id)
    
    diagnosisDb = Diagnosis.objects.using('db_diagnosis').filter(id=id)
    prescriptionsDb = Prescription.objects.using('db_prescription').filter(id = id)
    treatmentsDb = Treatment.objects.using('db_treatment').filter(id = id)
    dataToSend = {}
    print(diagnosisDb.get().diagnose)
    dataForHospitalPii = []
    dataForHospitalVs = []
    dataForDiagnosis = []
    dataForPrescriptions = []
    dataForTreatments = []
    
    for i in attributes:
        if i in hospitalPii: dataForHospitalPii.append(i)
        if i in hospitalVs: dataForHospitalVs.append(i)
        if i in diagnosis: dataForDiagnosis.append(i)
        if i in prescriptions: dataForPrescriptions.append(i)
        if i in treatments: dataForTreatments.append(i)
    
    for r in dataForHospitalPii:  dataToSend[r] = person.values_list(r)[0][0]
    for r in dataForHospitalVs: dataToSend[r] = vitalSigns.values_list(r)[0][0]
    for r in dataForDiagnosis: dataToSend[r] = diagnosisDb.values_list(r)[0][0]
    for r in dataForPrescriptions: dataToSend[r] = prescriptionsDb.values_list(r)[0][0]
    for r in dataForTreatments: dataToSend[r] = treatmentsDb.values_list(r)[0][0]
    
    toInsert = int(ssn), str(attributes), froms[0], tos[0]
    updateLinkingDatabase('INSERT INTO linking(userId, attributes, froms, tos) VALUES(?,?,?,?)', './hospital_api/Links.db', toInsert)
    return JsonResponse(dataToSend, safe=False)
    

def inform(request):
    if request.method != 'GET':
        return HttpResponse("Bad Request", status=status.HTTP_400_BAD_REQUEST)
    
    attributes = request.GET.getlist('attributes')
    froms = request.GET.getlist('froms')
    tos = request.GET.getlist('tos')
    ssn = request.GET['ssn']

    toInsert = (int(ssn), str(attributes), (froms[0]), (tos[0]))
    print(toInsert)
    updateLinkingDatabase('INSERT INTO linking(userId, attributes, froms, tos) VALUES(?,?,?,?)', './hospital_api/Links.db', toInsert)
    return HttpResponse(200)


def updatedatadetails(request):
    if request.method != 'POST':
        return HttpResponse("Bad Request", status=status.HTTP_400_BAD_REQUEST)