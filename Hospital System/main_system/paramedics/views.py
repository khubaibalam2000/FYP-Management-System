from django.shortcuts import render
import requests
import sqlite3
import json
from django.http import HttpResponse, JsonResponse

def updateDatabase(queryOfLink, dbPath, toInsert):
    connection = sqlite3.connect(dbPath)
    cursor = connection.cursor()
    cursor.execute(queryOfLink, toInsert)
    connection.commit()
    connection.close()

# Create your views here.
def requestMOHForData(request):
    attributes = request.GET.getlist('attributes')
    dataToGet = {}
    dataToGet['ssn'] = str(request.GET['ssn'])
    dataToGet['froms'] = 'MinistryOfHealth'
    dataToGet['tos'] = 'Paramedics'

    for i in attributes:
        if 'attributes' in dataToGet.keys():
            dataToGet['attributes'].append(i)
            continue
        dataToGet['attributes'] = [i]
    response = requests.get('http://127.0.0.1:8000/moh/sendToParamedics', params = dataToGet)
    data = response.json()
    stringData = json.dumps(data)
    toInsert = request.GET['ssn'], stringData
    updateDatabase('INSERT INTO data(ssn, data) VALUES(?,?)', './paramedics/datas.db', toInsert)
    return JsonResponse(data)