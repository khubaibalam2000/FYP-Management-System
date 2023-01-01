from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import requests
import sqlite3
import json

def updateDatabase(queryOfLink, dbPath, toInsert):
    connection = sqlite3.connect(dbPath)
    cursor = connection.cursor()
    cursor.execute(queryOfLink, toInsert)
    connection.commit()
    connection.close()

def getDataFromDB(dbName, query):
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()
    connection.commit()
    connection.close()
    return rows

# Create your views here.
def requestData(request):

    attributes = request.GET.getlist('attributes')

    dataToGet = {}
    dataToGet['ssn'] = str(request.GET['ssn'])
    dataToGet['froms'] = 'Hospital'
    dataToGet['tos'] = 'MinistryOfHealth'
    for i in attributes:
        if 'attributes' in dataToGet.keys():
            dataToGet['attributes'].append(i)
            continue
        dataToGet['attributes'] = [i]
    response = requests.get('http://127.0.0.1:8000/datadetails/personal/requestForData', params = dataToGet)
    data = response.json()
    stringData = json.dumps(data)
    toInsert = request.GET['ssn'], stringData
    updateDatabase('INSERT INTO data(ssn, data) VALUES(?,?)', './ministry_of_health/datas.db', toInsert)
    return JsonResponse(data)

def sendToParamedics(request):
    attributes = request.GET.getlist('attributes')
    dataToGet = {}
    dataToGet['ssn'] = request.GET['ssn']
    dataToGet['froms'] = 'MinistryOfHealth'
    dataToGet['tos'] = 'Paramedics'
    
    for i in attributes:
        if 'attributes' in dataToGet.keys():
            dataToGet['attributes'].append(i)
            continue
        dataToGet['attributes'] = [i]

    data = getDataFromDB('./ministry_of_health/datas.db', 'select data from data where ssn = ' + str(request.GET['ssn']))
    listOfDict = []
    for i in data:
        listOfDict.append(json.loads(i[0]))
    dataToSend = {}

    checkAttributes = []
    for i in attributes:
        for j in listOfDict:
            for key, values in j.items():
                if i == key:
                    checkAttributes.append(i)
    
    checkAttributes = list(set(checkAttributes))
    requestFromHospital = []
    for i in attributes:
        if i not in checkAttributes:
            requestFromHospital.append(i)
            # return HttpResponse('We do not have that data')
    dataFromHospital = {}
    dataFromHospital['ssn'] = request.GET['ssn']
    dataFromHospital['froms'] = 'MinistryOfHealth'
    dataFromHospital['tos'] = 'Paramedics'

    for i in requestFromHospital:
        if 'attributes' in dataFromHospital.keys():
            dataFromHospital['attributes'].append(i)
            continue
        dataFromHospital['attributes'] = [i]
    if requestFromHospital:
        response = requests.get('http://127.0.0.1:8000/datadetails/personal/requestForData', params = dataFromHospital)
        data = response.json()
    for i in attributes:
        for j in listOfDict:
            for key, values in j.items():
                if i == key:
                    dataToSend[i] = values
    dictForInformHospital = {}
    if requestFromHospital:
        for key, values in data.items():
            dictForInformHospital[key] = values
            dataToSend[key] = values
    dictForInformHospital['ssn'] = request.GET['ssn']
    dictForInformHospital['froms'] = 'MinistryOfHealth'
    dictForInformHospital['tos'] = 'Paramedics'
    for i in checkAttributes:
        if 'attributes' in dictForInformHospital.keys():
            dictForInformHospital['attributes'].append(i)
            continue
        dictForInformHospital['attributes'] = [i]
    if checkAttributes:
        response = requests.get('http://127.0.0.1:8000/datadetails/personal/inform', params = dictForInformHospital)
    return JsonResponse(dataToSend)