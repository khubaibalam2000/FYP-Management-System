from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import requests
import sqlite3
import json
from datetime import datetime
from jsonmerge import merge
from datetime import timedelta

def updateDatabase(queryOfLink, dbPath, toInsert=None):
    connection = sqlite3.connect(dbPath)
    cursor = connection.cursor()
    if toInsert:
        cursor.execute(queryOfLink, toInsert)
    else: 
        cursor.execute(queryOfLink)
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

    # check for policies
    policyFilters = {}
    policyFilters['ssn'] = str(request.GET['ssn'])
    policyFilters['entity'] = 'moh'
    for i in attributes:
            if 'attributes' in policyFilters.keys():
                policyFilters['attributes'].append(i)
                continue
            policyFilters['attributes'] = [i]

    response = requests.get('http://127.0.0.1:8000/datadetails/personal/checkpolicy', params = policyFilters)
    data = response.json()
    attributes = data['attributes']
    policies = data['policy_days']
    # print(policies)

    # data
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

    # time json
    time = {}
    for i in attributes:
        time[i] = datetime.now()
    # print(str(time))
    if getDataFromDB('./ministry_of_health/datas.db', 'select data from data where ssn = ' + str(request.GET['ssn'])):

        # update data
        old_data = getDataFromDB('./ministry_of_health/datas.db', 'select data from data where ssn = ' + str(request.GET['ssn']))
        # print(old_data[0][0])
        old_data_json = json.loads(old_data[0][0])
        result = merge(data, old_data_json)
        # print(result)
        stringifyResultData = json.dumps(result).replace("'", "")
        updateDatabase("update data set data = '" + stringifyResultData + "' where ssn = " + request.GET['ssn'], './ministry_of_health/datas.db')

        # update policies
        old_policy = getDataFromDB('./ministry_of_health/datas.db', 'select policy from data where ssn = ' + str(request.GET['ssn']))
        print(old_policy[0][0])
        old_policy_json = json.loads(old_policy[0][0])
        resultPolicy = merge(policies, old_policy_json)
        # print(resultPolicy)
        stringifyResultPolicy = json.dumps(resultPolicy).replace("'", "")
        updateDatabase("update data set policy = '" + stringifyResultPolicy + "' where ssn = " + request.GET['ssn'], './ministry_of_health/datas.db')

        # update times
        old_time = getDataFromDB('./ministry_of_health/datas.db', 'select received_at from data where ssn = ' + str(request.GET['ssn']))
        print(old_time[0][0])
        old_time_json = json.loads(old_time[0][0])
        resultTime = merge(time, old_time_json)
        # print(resultPolicy)
        stringifyResultTime = json.dumps(resultTime, default=str)
        # stringifyResultTime = json.dumps(resultTime).replace("'", "")
        updateDatabase("update data set received_at = '" + stringifyResultTime + "' where ssn = " + request.GET['ssn'], './ministry_of_health/datas.db')
    else:
        stringData = json.dumps(data)
        toInsert = request.GET['ssn'], stringData, json.dumps(policies), json.dumps(time, default=str)
        updateDatabase('INSERT INTO data(ssn, data, policy, received_at) VALUES(?,?,?,?)', './ministry_of_health/datas.db', toInsert)
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

def deleteDataBasedOnPolicy(request):
    result = getDataFromDB('./ministry_of_health/datas.db', 'select data, policy, received_at from data where ssn = ' + str(request.GET['ssn']))
    print(result)
    data = json.loads(result[0][0])
    policy = json.loads(result[0][1])
    time = json.loads(result[0][2])
    print(data, policy, time)
    for key, value in list(data.items()):
        when_to_delete = datetime.strptime(time[key], '%Y-%m-%d %H:%M:%S.%f') + timedelta(days = int(policy[key]))
        print(when_to_delete)
        if when_to_delete < datetime.now():
            data.pop(key, None)
            policy.pop(key, None)
            time.pop(key, None)
            updateDatabase("update data set data = '" + json.dumps(data) + "' where ssn = " + request.GET['ssn'], './ministry_of_health/datas.db')
            updateDatabase("update data set policy = '" + json.dumps(policy) + "' where ssn = " + request.GET['ssn'], './ministry_of_health/datas.db')
            updateDatabase("update data set received_at = '" + json.dumps(time) + "' where ssn = " + request.GET['ssn'], './ministry_of_health/datas.db')

    return HttpResponse(200)