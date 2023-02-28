from django.shortcuts import render
import requests
import sqlite3
import json
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from jsonmerge import merge
from datetime import timedelta
import random as rn
import networkx as nx
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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
    if response.content == b"We do not have that person's data": return HttpResponse("Hospital do not have that person's data")
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





    # time json
    time = {}
    for i in attributes:
        time[i] = datetime.now()
    # print(str(time))
    if getDataFromDB('./paramedics/datas.db', 'select data from data where ssn = ' + str(request.GET['ssn'])):

        # update data
        old_data = getDataFromDB('./paramedics/datas.db', 'select data from data where ssn = ' + str(request.GET['ssn']))
        # print(old_data[0][0])
        old_data_json = json.loads(old_data[0][0])
        result = merge(data, old_data_json)
        # print(result)
        stringifyResultData = json.dumps(result).replace("'", "")
        updateDatabase("update data set data = '" + stringifyResultData + "' where ssn = " + request.GET['ssn'], './paramedics/datas.db')

        # update policies
        old_policy = getDataFromDB('./paramedics/datas.db', 'select policy from data where ssn = ' + str(request.GET['ssn']))
        print(old_policy[0][0])
        old_policy_json = json.loads(old_policy[0][0])
        resultPolicy = merge(policies, old_policy_json)
        # print(resultPolicy)
        stringifyResultPolicy = json.dumps(resultPolicy).replace("'", "")
        updateDatabase("update data set policy = '" + stringifyResultPolicy + "' where ssn = " + request.GET['ssn'], './paramedics/datas.db')

        # update times
        old_time = getDataFromDB('./paramedics/datas.db', 'select received_at from data where ssn = ' + str(request.GET['ssn']))
        print(old_time[0][0])
        old_time_json = json.loads(old_time[0][0])
        resultTime = merge(time, old_time_json)
        # print(resultPolicy)
        stringifyResultTime = json.dumps(resultTime, default=str)
        # stringifyResultTime = json.dumps(resultTime).replace("'", "")
        updateDatabase("update data set received_at = '" + stringifyResultTime + "' where ssn = " + request.GET['ssn'], './paramedics/datas.db')
    else:
        stringData = json.dumps(data)
        toInsert = request.GET['ssn'], stringData, json.dumps(policies), json.dumps(time, default=str)
        updateDatabase('INSERT INTO data(ssn, data, policy, received_at) VALUES(?,?,?,?)', './paramedics/datas.db', toInsert)
    return JsonResponse(data)





    # stringData = json.dumps(data)
    # toInsert = request.GET['ssn'], stringData
    # updateDatabase('INSERT INTO data(ssn, data) VALUES(?,?)', './paramedics/datas.db', toInsert)
    # return JsonResponse(data)

def deleteParamedicsData(request):
    ssn = request.GET['ssn']
    getDataFromDB('./paramedics/datas.db', "delete from data where ssn = " + str(ssn))
    return HttpResponse("Data deleted from paramedics")

def deleteDataBasedOnPolicyParamedics(request):
    result = getDataFromDB('./paramedics/datas.db', 'select data, policy, received_at from data where ssn = ' + str(request.GET['ssn']))
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
            updateDatabase("update data set data = '" + json.dumps(data) + "' where ssn = " + request.GET['ssn'], './paramedics/datas.db')
            updateDatabase("update data set policy = '" + json.dumps(policy) + "' where ssn = " + request.GET['ssn'], './paramedics/datas.db')
            updateDatabase("update data set received_at = '" + json.dumps(time) + "' where ssn = " + request.GET['ssn'], './paramedics/datas.db')

    return HttpResponse(200)

def updatePolicyPara(request):
    response = request.body.decode('UTF-8')
    policy_atts = response.split('&')
    ssn = request.GET['ssn']

    # print(policy_atts)
    policy_duration = {}
    for i in policy_atts:
        equal_divide = i.split('=')
        policy_duration[equal_divide[0]] = equal_divide[1]
    print(policy_duration)
    updateDatabase("update data set policy = '" + json.dumps(policy_duration) + "' where ssn = " + ssn, './paramedics/datas.db')

    return HttpResponse(200)


def generatePDGPara(request):
    ssn = request.GET['ssn']

    linkData = getDataFromDB('./paramedics/Linkspara.db', 'select * from linking where userId = ' + str(ssn))

    dictForData = {}
    for i in linkData:
        if (i[3], i[4]) in dictForData:
            a = dictForData[(i[3], i[4])]
            a += i[2]
            dictForData[(i[3], i[4])] = a
            continue
        dictForData[(i[3], i[4])] = i[2]

    E = []
    pos = {}
    for key, values in dictForData.items():
        inList = []
        inList.extend(re.findall(r"'(.*?)'", values))
        inList = list(set(inList))
        E.append((key[0], key[1], inList))
        pos[key[0]] = [rn.randint(0,10), rn.randint(0,10)]
        pos[key[1]] = [rn.randint(0,10), rn.randint(0,10)]
    G = nx.DiGraph()
    G.add_weighted_edges_from(E)
    weight = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos=pos, with_labels=True, node_size=1000, node_color='b', edge_color='g', arrowsize=35)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weight)
    
    response = HttpResponse(content_type='image/png')
    plt.gcf().set_size_inches(20, 10)
    plt.savefig(response, format='png')
    plt.clf()
    return response
