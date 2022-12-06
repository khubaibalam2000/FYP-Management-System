from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from .models import *

USE_DB = 'db_prescription'

def index(request):
    if request.method != "GET":
        return HttpResponse("Bad Request", status=status.HTTP_400_BAD_REQUEST)
    
    print("A")
    pres = Prescription.objects.using(USE_DB).all()
    print("B")
    serializer = PrescriptionSerializer(pres, many=True)
    print("C")
    return JsonResponse(serializer.data, safe=False)

def get(request):
    if request.method != "GET":
        return HttpResponse("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    try:
        pres = Prescription.objects.using(USE_DB).get(id=request.GET['id'])
    except:
        return HttpResponse("Not Found", status=status.HTTP_404_NOT_FOUND)

    serializer = PrescriptionSerializer(pres)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET', 'POST'])
def add(request):
    serializer = PrescriptionSerializer(data=request.data)
    if serializer.is_valid():
        if request.data != {}:
            serializer.save()
        return Response(serializer.data)
    else:
        return HttpResponse("Bad Data", status=status.HTTP_400_BAD_REQUEST)