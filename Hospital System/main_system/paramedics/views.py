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

def getDataFromDB(dbName, query):
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()
    connection.commit()
    connection.close()
    return rows

# Create your views here.
def requestMOHForData(request):
    attributes = request.GET.getlist('attributes')
    
    # check for policies
    policyFilters = {}
    policyFilters['ssn'] = str(request.GET['ssn'])
    policyFilters['entity'] = 'paramedics'
    for i in attributes:
            if 'attributes' in policyFilters.keys():
                policyFilters['attributes'].append(i)
                continue
            policyFilters['attributes'] = [i]

    response = requests.get('http://127.0.0.1:8000/datadetails/personal/checkpolicy', params = policyFilters)
    print(response.json())
    data = response.json()
    print(data)
    attributes = data['attributes']
    policies = data['policy_days']
    print(policies)

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


def deleteParamedicsData(request):
    ssn = request.GET['ssn']
    getDataFromDB('./paramedics/datas.db', "delete from data where ssn = " + str(ssn))

    return HttpResponse("Data deleted from paramedics")