from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from .models import *
import sqlite3

USE_DB = 'db_treatment'

def getDataFromDB(dbName, query):
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()
    connection.commit()
    connection.close()
    return rows

def index(request):
    if request.method != "GET":
        return HttpResponse("Bad Request", status=status.HTTP_400_BAD_REQUEST)
    
    treat = Treatment.objects.using(USE_DB).all()
    serializer = TreatmentSerializer(treat, many=True)
    return JsonResponse(serializer.data, safe=False)

def get(request):
    if request.method != "GET":
        return HttpResponse("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    try:
        treat = Treatment.objects.using(USE_DB).get(id=request.GET['id'])
    except:
        return HttpResponse("Not Found", status=status.HTTP_404_NOT_FOUND)

    serializer = TreatmentSerializer(treat)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET', 'POST'])
def add(request):
    serializer = TreatmentSerializer(data=request.data)
    if serializer.is_valid():
        if request.data != {}:
            serializer.save()
        return Response(serializer.data)
    else:
        return HttpResponse("Bad Data", status=status.HTTP_400_BAD_REQUEST)
    
def deleteDataTreatment(request):
    id = request.GET['id']
    getDataFromDB('./treatment/treatmentsDb.sqlite3', 'delete from treatments where id = ' + str(id))

    return HttpResponse("Data Deleted from Treatment")