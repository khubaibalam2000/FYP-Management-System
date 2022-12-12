from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from .models import *
import sqlite3

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

    requirements = request.GET.getlist('attributes')
    froms = request.GET.getlist('froms')
    tos = request.GET.getlist('tos')
    ssn = request.GET['ssn']
    person = PersonalInfo.objects.filter(ssn=request.GET['ssn'])
    dataToSend = []
    for r in requirements:
        dataToSend.append(person.values_list(r)[0][0])
    toInsert = (int(ssn), str(requirements), str(froms), str(tos))
    updateLinkingDatabase('INSERT INTO linking(userId, attributes, froms, tos) VALUES(?,?,?,?)', 'D:\Semesters\Semester VII\FYP\FYP-Management-System\Data-Files\DB-Files\Links.db', toInsert)
    return JsonResponse(dataToSend, safe=False)

def inform(request):
    if request.method != 'GET':
        return HttpResponse("Bad Request", status=status.HTTP_400_BAD_REQUEST)
    
    attributes = request.GET.getlist('attributes')
    froms = request.GET.getlist('froms')
    tos = request.GET.getlist('tos')
    ssn = request.GET.getlist('ssn')


    toInsert = (int(ssn), str(attributes), str(froms), str(tos))
    updateLinkingDatabase('INSERT INTO linking(userId, attributes, froms, tos) VALUES(?,?,?,?)', 'D:\Semesters\Semester VII\FYP\FYP-Management-System\Data-Files\DB-Files\Links.db', toInsert)
    return HttpResponse(200)


def updatedatadetails(request):
    if request.method != 'POST':
        return HttpResponse("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    


