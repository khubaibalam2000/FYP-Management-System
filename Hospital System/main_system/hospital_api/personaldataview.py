from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random as rn
import networkx as nx
from .serializers import *
from .models import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sqlite3
from diagnosis.models import Diagnosis
from prescription.models import Prescription
from treatment.models import Treatment
import pandas as pd
import plotly.express as px
from django.template import loader
from pathlib import Path
from matplotlib.backends.backend_pdf import PdfPages
from wsgiref.util import FileWrapper
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Table
from reportlab.platypus import Spacer, Paragraph
import re
import json
from . import multichain
from Savoir import Savoir
import requests
from datetime import datetime
import time
import threading
import os

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
    if not person: return HttpResponse("We do not have that data")
    id = person.values_list('id')[0][0]

    vitalSigns = VitalSigns.objects.filter(id = id)
    
    diagnosisDb = Diagnosis.objects.using('db_diagnosis').filter(id=id)
    prescriptionsDb = Prescription.objects.using('db_prescription').filter(id = id)
    treatmentsDb = Treatment.objects.using('db_treatment').filter(id = id)
    dataToSend = {}
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
    froms = request.GET['froms']
    tos = request.GET['tos']
    ssn = request.GET['ssn']

    toInsert = int(ssn), str(attributes), (froms), (tos)
    updateLinkingDatabase('INSERT INTO linking(userId, attributes, froms, tos) VALUES(?,?,?,?)', './hospital_api/Links.db', toInsert)
    return HttpResponse(200)


def updateDatabase(queryOfLink, dbPath, toInsert=None):
    connection = sqlite3.connect(dbPath, timeout=10)
    cursor = connection.cursor()
    if toInsert:
        cursor.execute(queryOfLink, toInsert)
    else: 
        cursor.execute(queryOfLink)
    connection.commit()
    connection.close()
    # cursor.close()

def getDataFromDB(dbName, query):
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()
    connection.commit()
    connection.close()
    # cursor.close()
    return rows

def generateExternalPDGWithConnections(request):
    ssn = request.GET['ssn']

    linkData = getDataFromDB('./hospital_api/Links.db', 'select * from linking where userId = ' + str(ssn))

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
    nx.draw(G, pos=pos, with_labels=True, node_size=1000, node_color='r', edge_color='g', arrowsize=35)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weight)
    
    response = HttpResponse(content_type='image/png')
    plt.gcf().set_size_inches(20, 10)
    plt.savefig(response, format='png')
    plt.clf()
    return response

def generateExternalPDGWithoutConnections(request):
    ssn = request.GET['ssn']
    
    linkData = getDataFromDB('./hospital_api/Links.db', 'select * from linking where userId = ' + str(ssn))
    # print(linkData)
    x = []
    y = []
    for i in range(3): x.append(rn.randint(0,6))
    for i in range(3): y.append(rn.randint(0,6))

    dictForData = {}
    for i in linkData:
        if (i[3], i[4]) in dictForData:
            a = dictForData[(i[3], i[4])]
            a += i[2]
            dictForData[(i[3], i[4])] = a
            continue
        dictForData[(i[3], i[4])] = i[2]
    externalEntities = []
    for key, value in dictForData.items():
        externalEntities.append(key[0])
        externalEntities.append(key[1])
    externalEntities = list(set(externalEntities))
    attributesData = []

    for i in externalEntities:
        if i == 'Hospital':
            attributesData.append(['name', 'dob', 'city', 'province', 'gender', 'email', 'phone', 'ssn', 'heart_rate', 'blood_pressure', 'respiration_rate', 'oxygen_saturation', 'temperature', 'diagnose', 'medicine', 'treatment'])
            continue
        attributesData.append(getDataFromDB('./hospital_api/Links.db', 'select attributes from linking where (userId = ' + str(ssn) + ") and (froms = '" + i + "' OR tos = '" + i + "')"))
    
    fAtt = []
    for i in attributesData:
        inList = []
        for j in i:
            for k in j:
                inList.extend(re.findall(r"'(.*?)'", k))
        inList = list(set(inList))
        fAtt.append(inList)

    for i in fAtt:
        if not i:
            idx = fAtt.index(i)
            fAtt[idx] = ['name', 'dob', 'city', 'province', 'gender', 'email', 'phone', 'ssn', 'heart_rate', 'blood_pressure', 'respiration_rate', 'oxygen_saturation', 'temperature', 'diagnose', 'medicine', 'treatment']

    frame = {'x': x, 'y': y, 'External Entity': externalEntities, 'Attributes': fAtt}
    print(len(x), len(y), len(externalEntities), len(fAtt), '============================')
    df = pd.DataFrame(frame)
    fig = px.scatter(df, x="x", y="y", color="External Entity", hover_data={'x': False, 'y': False, 'External Entity':True, 'Attributes':True})
    fig.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
    
    fig.write_html("./hospital_api/templates/epdgwithoutC.html")
    
    template = loader.get_template("./epdgwithoutC.html")
    return HttpResponse(template.render())

def makeDataFrameForUser(pii, diagnosis, medicines, habits, allergens, vs, treats, surgeries, immunizations):
    x = []
    y = []
    for i in range(4): x.append(rn.randint(0,6))
    for i in range(4): y.append(rn.randint(0,6))
    entity = ['hospital', 'diagnose', 'prescriptions', 'treatments']
    data = [str(pii)+str(vs), str(diagnosis), str(medicines)+str(habits)+str(allergens), str(treats)+str(surgeries)+str(immunizations)]
    size = [1, 2, 4, 3]
    frame = {'x': x, 'y': y, 'entity': entity, 'size': size, 'data': data}
    return frame

def internalPDG(request):
    userId = request.GET['id']
    if int(userId) < 1 or int(userId) > 999:
        return HttpResponse("We do not have that person data")
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = str(BASE_DIR)
    path = path[0:len(path)-27]
    pii = getDataFromDB(path + './Data-Files/DB-Files/piiDb.db', 'select * from personal_info where id = ' + str(userId))
    diagnosis = getDataFromDB(path + './Data-Files/DB-Files/diagnosisDb.db', 'select * from diagnosis where id = ' + str(userId))
    medicines = getDataFromDB(path + './Data-Files/DB-Files/prescriptionsDb.db', 'select * from medicines where id = ' + str(userId))
    habits = getDataFromDB(path + './Data-Files/DB-Files/habitsDb.db', 'select * from habits where id = ' + str(userId))
    allergens = getDataFromDB(path + './Data-Files/DB-Files/allergyDb.db', 'select * from allergies where id = ' + str(userId))
    vs = getDataFromDB(path + './Data-Files/DB-Files/vitalSignsDb.db', 'select * from vital_signs where id = ' + str(userId))
    treats = getDataFromDB(path + './Data-Files/DB-Files/treatmentsDb.db', 'select * from treatments where id = ' + str(userId))
    surgeries = getDataFromDB(path + './Data-Files/DB-Files/surgeryDb.db', 'select * from surgeries where id = ' + str(userId))
    immunizations = getDataFromDB(path + './Data-Files/DB-Files/immunizationsDb.db', 'select * from immunizations where id = ' + str(userId))

    dictForUser = makeDataFrameForUser(pii, diagnosis, medicines, habits, allergens, vs, treats, surgeries, immunizations)
    df = pd.DataFrame(dictForUser)

    fig = px.scatter(df, x="entity", y="y", color="entity", size='size', hover_data={'x':False, 'y':False, 'entity':True, 'size': False, 'data':True})
    fig.write_html("./hospital_api/templates/ipdg.html")
    
    template = loader.get_template("./ipdg.html")
    return HttpResponse(template.render())

def eXdataReport(request):
    ssn = request.GET['ssn']

    linkData = getDataFromDB('./hospital_api/Links.db', 'select * from linking where userId = ' + str(ssn))
    # print(linkData)
    if not linkData:
        return HttpResponse('This subjects data is not shared with anyone')
    dictForData = {}
    for i in linkData:
        if (i[3], i[4]) in dictForData:
            a = dictForData[(i[3], i[4])]
            a += i[2]
            dictForData[(i[3], i[4])] = a
            continue
        dictForData[(i[3], i[4])] = i[2]
    exchangers = []
    data = []

    for key, values in dictForData.items():
        inList = []
        exchangers.append(key)
        inList.extend(re.findall(r"'(.*?)'", values))
        inList = list(set(inList))
        data.append(inList)
    frame = {'Exchanging Entites': exchangers, 'Exchanged Data': data}
    df = pd.DataFrame(frame)

    fig, ax = plt.subplots(figsize=(12,4))
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center', colColours=['green', 'green'], cellLoc='center')
    the_table[(2,0)].set_facecolor('#D3D3D3')
    the_table[(2,1)].set_facecolor('#D3D3D3')
    pp = PdfPages("ExternalExchangedData.pdf")
    pp.savefig(fig, bbox_inches='tight')
    pp.close()

    short_report = open("ExternalExchangedData.pdf", 'rb')
    response = HttpResponse(FileWrapper(short_report), content_type='application/pdf')
    return response

def eHdataReport(request):
    ssn = request.GET['ssn']

    linkData = getDataFromDB('./hospital_api/Links.db', 'select * from linking where userId = ' + str(ssn))
    x = []
    y = []

    dictForData = {}
    for i in linkData:
        if (i[3], i[4]) in dictForData:
            a = dictForData[(i[3], i[4])]
            a += i[2]
            dictForData[(i[3], i[4])] = a
            continue
        dictForData[(i[3], i[4])] = i[2]
    externalEntities = []
    for key, value in dictForData.items():
        externalEntities.append(key[0])
        externalEntities.append(key[1])
    externalEntities = list(set(externalEntities))
    attributesData = []

    userIdForDataExtraction = getDataFromDB('./db.sqlite3', 'select id from personal_info where ssn = ' + str(ssn))
    userIdForDataExtraction = userIdForDataExtraction[0][0]

    hospitalPiiAttributes = getDataFromDB('./db.sqlite3', 'select * from personal_info where id = ' + str(userIdForDataExtraction))
    hospitalVsAttributes = getDataFromDB('./db.sqlite3', 'select * from vital_signs where id = ' + str(userIdForDataExtraction))
    diagnosisAttributes = getDataFromDB('./diagnosis/diagnosisDb.sqlite3', 'select * from diagnosis where id = ' + str(userIdForDataExtraction))
    prescriptionsAttributes = getDataFromDB('./prescription/prescriptionsDb.sqlite3', 'select * from medicines where id = ' + str(userIdForDataExtraction))
    treatmentsAttributes = getDataFromDB('./treatment/treatmentsDb.sqlite3', 'select * from treatments where id = ' + str(userIdForDataExtraction))

    
    hospitalPiiColumns = ['id', 'name', 'dob', 'city', 'province', 'gender', 'email', 'phone', 'ssn']
    hospitalVsColumns = ['id', 'heart_rate', 'blood_pressure', 'respiration_rate', 'oxygen_saturation', 'temperature']
    diagnosisColumns = ['id', 'diagnose']
    prescriptionColumns = ['id', 'medicine']
    treatmentColumns = ['id', 'treatment']

    hospitalPiiMapper = {}
    hospitalVsMapper = {}
    diagnosisMapper = {}
    prescriptionMapper = {}
    treatmentMapper = {}

    for idx, value in enumerate(hospitalPiiColumns): hospitalPiiMapper[value] = hospitalPiiAttributes[0][idx]
    for idx, value in enumerate(hospitalVsColumns): hospitalVsMapper[value] = hospitalVsAttributes[0][idx]
    for idx, value in enumerate(diagnosisColumns): diagnosisMapper[value] = diagnosisAttributes[0][idx]
    for idx, value in enumerate(prescriptionColumns): prescriptionMapper[value] = prescriptionsAttributes[0][idx]
    for idx, value in enumerate(treatmentColumns): treatmentMapper[value] = treatmentsAttributes[0][idx]
    
    listForHospital = []
    for key, value in hospitalPiiMapper.items(): 
        if value != 'None': listForHospital.append(key)
    for key, value in hospitalVsMapper.items():
        if value != 'None': listForHospital.append(key)
    for key, value in diagnosisMapper.items():
        if value != 'None': listForHospital.append(key)
    for key, value in prescriptionMapper.items():
        if value != 'None': listForHospital.append(key)
    for key, value in treatmentMapper.items():
        if value != 'None': listForHospital.append(key)
    
    while 'id' in listForHospital:
        listForHospital.remove('id')

    for i in externalEntities:
        if i == 'Hospital':
            attributesData.append(listForHospital)
            continue
        attributesData.append(getDataFromDB('./hospital_api/Links.db', 'select attributes from linking where (userId = ' + str(ssn) + ") and (froms = '" + i + "' OR tos = '" + i + "')"))
    
    fAtt = []
    for i in attributesData:
        inList = []
        for j in i:
            for k in j:
                inList.extend(re.findall(r"'(.*?)'", k))
        inList = list(set(inList))
        fAtt.append(inList)




    for i in fAtt:
            if not i:
                idx = fAtt.index(i)
                fAtt[idx] = listForHospital

    frame = {'External Entity': externalEntities, 'Attribute': fAtt}
    df = pd.DataFrame(frame)
    
    fig, ax = plt.subplots(figsize=(25, 4))
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center', cellLoc='center', colColours=['green', 'green'], colWidths=[0.1, 1])
    the_table[(2,0)].set_facecolor('#D3D3D3')
    the_table[(2,1)].set_facecolor('#D3D3D3')

    pp = PdfPages("HoldingDataEntities.pdf")
    pp.savefig(fig, bbox_inches='tight')
    pp.close()

    short_report = open("HoldingDataEntities.pdf", 'rb')
    response = HttpResponse(FileWrapper(short_report), content_type='application/pdf')
    return response

def organizeDataForReport(pii, vs, diagnosis, medicines,  treats, listPii, listVS, listDiag, listMeds, listTreats):
    if pii:
        listPii.append(['id', 'name', 'DOB', 'city', 'province', 'gender', 'email', 'phone', 'ssn'])
        listPii.append(list(pii[0]))

    if vs:
        listVS.append(['id', 'Heart_Rate', 'Blood_Pressure', 'Respiration_Rate', 'Oxygen_Saturation', 'Temperature'])
        listVS.append(list(vs[0]))

    if diagnosis:
        listDiag.append(['id', 'diagnose'])
        listDiag.append(list(diagnosis[0]))

    if medicines:
        listMeds.append(['id', 'medicines'])
        listMeds.append(list(medicines[0]))

    if treats:
        listTreats.append(['id', 'treatments'])
        listTreats.append(list(treats[0]))

elems = []
fileName = 'InternalReportSummary.pdf'
pdf = SimpleDocTemplate(
    fileName,
    pagesize=letter
)

def generateReportSummary(data):
    table = Table(data)
    # add style
    style = TableStyle([
        ('BACKGROUND', (0,0), (len(data[0]),0), colors.green),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),

        ('ALIGN',(0,0),(-1,-1),'CENTER'),

        ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),

        ('BOTTOMPADDING', (0,0), (-1,0), 12),

        ('BACKGROUND',(0,1),(-1,-1),colors.beige),
    ])
    table.setStyle(style)

    # 2) Alternate backgroud color
    rowNumb = len(data)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.burlywood
        else:
            bc = colors.beige
        
        ts = TableStyle(
            [('BACKGROUND', (0,i),(-1,i), bc)]
        )
        table.setStyle(ts)

    # 3) Add borders
    ts = TableStyle(
        [
        ('BOX',(0,0),(-1,-1),2,colors.black),

        ('LINEBEFORE',(2,1),(2,-1),2,colors.red),
        ('LINEABOVE',(0,2),(-1,2),2,colors.green),

        ('GRID',(0,1),(-1,-1),2,colors.black),
        ]
    )
    table.setStyle(ts)
    elems.append(table)
    line = Spacer(0,20)
    elems.append(line)

def iReport(request):

    userId = request.GET['id']
    if int(userId) < 1 or int(userId) > 999:
        return HttpResponse("We do not have that person data")
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = str(BASE_DIR)
    path = path[0:len(path)-27]

    pii, vs, diagnosis, medicines, treats = [], [], [], [], []
    pii = getDataFromDB('./db.sqlite3', 'select * from personal_info where id = ' + str(userId))
    vs = getDataFromDB('./db.sqlite3', 'select * from vital_signs where id = ' + str(userId))
    diagnosis = getDataFromDB('./diagnosis/diagnosisDb.sqlite3', 'select * from diagnosis where id = ' + str(userId))
    medicines = getDataFromDB('./prescription/prescriptionsDb.sqlite3', 'select * from medicines where id = ' + str(userId))
    treats = getDataFromDB('./treatment/treatmentsDb.sqlite3', 'select * from treatments where id = ' + str(userId))
    
    listPii, listDiag, listMeds, listVS, listTreats = [], [], [], [], []
    organizeDataForReport(pii, vs, diagnosis, medicines,  treats, listPii, listVS, listDiag, listMeds,  listTreats)
    print(listPii, listVS, listDiag, listMeds, listTreats)
    p = Paragraph('Report Summary', 
        ParagraphStyle('okay', fontName='Helvetica', fontSize=30)
    )
    elems.append(p)
    elems.append(Spacer(20,40))
    p = Paragraph('Hospital', 
        ParagraphStyle('okay', fontName='Helvetica', fontSize=22)
    )
    elems.append(p)
    elems.append(Spacer(20,10))
    p = Paragraph('Personal Data', 
        ParagraphStyle('okay', fontName='Helvetica', fontSize=15)
    )
    elems.append(p)
    elems.append(Spacer(20,10))
    generateReportSummary(listPii)

    p = Paragraph('Vital Signs Data', 
        ParagraphStyle('okay', fontName='Helvetica', fontSize=15)
    )
    elems.append(p)
    elems.append(Spacer(20,10))
    generateReportSummary(listVS)

    p = Paragraph('Diagnose Department', 
        ParagraphStyle('okay', fontName='Helvetica', fontSize=22)
    )
    elems.append(p)
    elems.append(Spacer(20,10))
    p = Paragraph('Diagnosis Data', 
        ParagraphStyle('okay', fontName='Helvetica', fontSize=15)
    )
    elems.append(p)
    elems.append(Spacer(20,10))
    generateReportSummary(listDiag)
    p = Paragraph('Prescriptions Department', 
        ParagraphStyle('okay', fontName='Helvetica', fontSize=22)
    )
    elems.append(p)
    elems.append(Spacer(20,10))
    p = Paragraph('Medicines Data', 
        ParagraphStyle('okay', fontName='Helvetica', fontSize=15)
    )
    elems.append(p)
    elems.append(Spacer(20,10))
    generateReportSummary(listMeds)
    p = Paragraph('Treatments Department', 
        ParagraphStyle('okay', fontName='Helvetica', fontSize=22)
    )
    elems.append(p)
    elems.append(Spacer(20,10))
    p = Paragraph('Treatments', 
        ParagraphStyle('okay', fontName='Helvetica', fontSize=15)
    )
    elems.append(p)
    elems.append(Spacer(20,10))
    generateReportSummary(listTreats)
    pdf.build(elems)

    short_report = open("InternalReportSummary.pdf", 'rb')
    response = HttpResponse(FileWrapper(short_report), content_type='application/pdf')
    return response

elems2 = []
fileName2 = 'DataBreachReport.pdf'
pdf2 = SimpleDocTemplate(
    fileName2,
    pagesize=letter
)


def generateReportSummaryForDataBreach(data):
    table = Table(data)
    # add style
    style = TableStyle([
        ('BACKGROUND', (0,0), (len(data[0]),0), colors.blue),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),

        ('ALIGN',(0,0),(-1,-1),'CENTER'),

        ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),

        ('BOTTOMPADDING', (0,0), (-1,0), 12),

        ('BACKGROUND',(0,1),(-1,-1),colors.white),
    ])
    table.setStyle(style)

    # 2) Alternate backgroud color
    rowNumb = len(data)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.white
        else:
            bc = colors.white
        
        ts = TableStyle(
            [('BACKGROUND', (0,i),(-1,i), bc)]
        )
        table.setStyle(ts)

    # 3) Add borders
    ts = TableStyle(
        [
        ('BOX',(0,0),(-1,-1),2,colors.black),

        ('LINEBEFORE',(2,1),(2,-1),2,colors.white),
        ('LINEABOVE',(0,2),(-1,2),2,colors.green),

        ('GRID',(0,1),(-1,-1),2,colors.black),
        ]
    )
    table.setStyle(ts)
    elems2.append(table)
    line = Spacer(0,20)
    elems2.append(line)

def dataBreachReport(request):
    userId = request.GET['id']
    if int(userId) < 1 or int(userId) > 999:
        return HttpResponse("We do not have that person data")
    departments = request.GET.getlist('departments')

    hospitalPiiAttributes, hospitalVsAttributes, diagnosisAttributes, prescriptionsAttributes, treatmentsAttributes = [], [], [], [], []
    listPii, listVs, listDiagnosis, listPrescriptions, listTreatments = [], [], [], [], []
    for i in departments:
        if i == 'Hospital' or i == 'hospital' or i == 'HOSPITAL':
            hospitalPiiAttributes = getDataFromDB('./db.sqlite3', 'select * from personal_info where id = ' + str(userId))
            hospitalVsAttributes = getDataFromDB('./db.sqlite3', 'select * from vital_signs where id = ' + str(userId))
        elif i == 'Diagnosis' or i == 'diagnosis' or i == 'DIAGNOSIS':
            diagnosisAttributes = getDataFromDB('./diagnosis/diagnosisDb.sqlite3', 'select * from diagnosis where id = ' + str(userId))
        elif i == 'Prescriptions' or i == 'prescriptions' or i == 'PRESCRIPTIONS':
            prescriptionsAttributes = getDataFromDB('./prescription/prescriptionsDb.sqlite3', 'select * from medicines where id = ' + str(userId))
        elif i == 'Treatments' or i == 'treatments' or i == 'TREATMENTS':
            treatmentsAttributes = getDataFromDB('./treatment/treatmentsDb.sqlite3', 'select * from treatments where id = ' + str(userId))
    
    organizeDataForReport(hospitalPiiAttributes, hospitalVsAttributes, diagnosisAttributes, prescriptionsAttributes, treatmentsAttributes, listPii, listVs, listDiagnosis, listPrescriptions, listTreatments)

    p = Paragraph('Data Breach Report', 
        ParagraphStyle('okay', fontName='Helvetica', fontSize=30)
    )
    elems2.append(p)
    elems2.append(Spacer(20,40))

    if hospitalPiiAttributes:
        p = Paragraph('Hospital', 
            ParagraphStyle('okay', fontName='Helvetica', fontSize=22)
        )
        elems2.append(p)
        elems2.append(Spacer(20,10))

        p = Paragraph('Personal Data', 
            ParagraphStyle('okay', fontName='Helvetica', fontSize=15)
        )
        elems2.append(p)
        elems2.append(Spacer(20,10))
        generateReportSummaryForDataBreach(listPii)

        p = Paragraph('Vital Signs Data', 
            ParagraphStyle('okay', fontName='Helvetica', fontSize=15)
        )
        elems2.append(p)
        elems2.append(Spacer(20,10))
        generateReportSummaryForDataBreach(listVs)

    if diagnosisAttributes:
        p = Paragraph('Diagnose Department', 
            ParagraphStyle('okay', fontName='Helvetica', fontSize=22)
        )
        elems2.append(p)
        elems2.append(Spacer(20,10))
        p = Paragraph('Diagnosis Data', 
            ParagraphStyle('okay', fontName='Helvetica', fontSize=15)
        )
        elems2.append(p)
        elems2.append(Spacer(20,10))
        generateReportSummaryForDataBreach(listDiagnosis)

    if prescriptionsAttributes:
        p = Paragraph('Prescriptions Department', 
            ParagraphStyle('okay', fontName='Helvetica', fontSize=22)
        )
        elems2.append(p)
        elems2.append(Spacer(20,10))
        p = Paragraph('Medicines Data', 
            ParagraphStyle('okay', fontName='Helvetica', fontSize=15)
        )
        elems2.append(p)
        elems2.append(Spacer(20,10))
        generateReportSummaryForDataBreach(listPrescriptions)
        

    if treatmentsAttributes:
        p = Paragraph('Treatments Department', 
            ParagraphStyle('okay', fontName='Helvetica', fontSize=22)
        )
        elems2.append(p)
        elems2.append(Spacer(20,10))
        p = Paragraph('Treatments', 
            ParagraphStyle('okay', fontName='Helvetica', fontSize=15)
        )
        elems2.append(p)
        elems2.append(Spacer(20,10))
        generateReportSummaryForDataBreach(listTreatments)

    pdf2.build(elems2)

    short_report = open("DataBreachReport.pdf", 'rb')
    response = HttpResponse(FileWrapper(short_report), content_type='application/pdf')
    return response

def storePoliciesOnMultiChain(request):
    rpchost = '127.0.0.1'
    rpcport = '6446'
    rpcuser = 'multichainrpc'
    rpcpassword = 'GJcB9QzPEMzpKb6j4L6SmPCX1Y62jjeXHGXS2xCVpiVF'
    chainname = 'chain1'
    mc = Savoir(rpcuser, rpcpassword, rpchost, rpcport, chainname)
    policy_json = json.loads(request.body)
    # txid = mc.create('stream', 'stream21', True)
    ssn = policy_json['ssn']
    txid = mc.publish("stream21", "key1", {"json" : policy_json})
    # print(txid)
    mc.subscribe('stream21')
    # print(mc.liststreamtxitems('stream21', txid))

    if getDataFromDB('./hospital_api/policy.db', 'select * from policy where ssn = ' + str(ssn)):
        updateDatabase("update policy set txid = '" + txid + "' where ssn = " + str(ssn), './hospital_api/policy.db')
        pdg = getDataFromDB('./hospital_api/Links.db', 'select * from linking where userId = ' + str(ssn))

        chainData = mc.liststreamtxitems('stream21', txid)[0]['data']['json']['attributes']
        if pdg:
            # print(pdg)
            dictForData = {}
            for i in pdg:
                if (i[3], i[4]) in dictForData and i[3] == 'Hospital' and i[4] == 'MinistryOfHealth':
                    a = dictForData[(i[3], i[4])]
                    a += i[2]
                    dictForData[(i[3], i[4])] = a
                    continue
                dictForData[(i[3], i[4])] = i[2]
            # print(dictForData)
            E = []
            pos = {}
            for key, values in dictForData.items():
                inList = []
                inList.extend(re.findall(r"'(.*?)'", values))
                inList = list(set(inList))
                E.append((key[0], key[1], inList))
            print(E)

            # print(chainData)
            policy_duration = {}
            for i in inList:
                for j in chainData:
                    if j['entity'] == i:
                        policy_duration[i] = j['duration']
            response = requests.get('http://127.0.0.1:8000/moh/updatepolicy', params = {'ssn': ssn, 'policy_duration': json.dumps(policy_duration)})
            # check link db which to organizations data of this ssn sent before

            # sent notification to those entities


    else:
        toInsert = (ssn, txid)
        updateDatabase('insert into policy(ssn, txid) VALUES(?,?)', './hospital_api/policy.db', toInsert)

    return HttpResponse(200)

def checkPoliciesOnMultiChain(request):
    ssn = request.GET['ssn']
    if not PersonalInfo.objects.filter(ssn=request.GET['ssn']): 
        return HttpResponse("We do not have that person's data")
    attributes = request.GET.getlist('attributes')

    txid = getDataFromDB('./hospital_api/policy.db', 'select txid from policy where ssn = ' + str(ssn))[0][0]
    
    rpchost = '127.0.0.1'
    rpcport = '6446'
    rpcuser = 'multichainrpc'
    rpcpassword = 'GJcB9QzPEMzpKb6j4L6SmPCX1Y62jjeXHGXS2xCVpiVF'
    chainname = 'chain1'
    mc = Savoir(rpcuser, rpcpassword, rpchost, rpcport, chainname)
    # txid = mc.create('stream', 'stream21', True)
    mc.subscribe('stream21')
    chainData = mc.liststreamtxitems('stream21', txid)[0]['data']['json']['attributes']
    # print(chainData)

    modifiedAttributes = []
    dictOfPolicyDays = {}
    for i in chainData:
        if i['entity'] in attributes:
            if i['sharing'] == 'yes' and i['sharing_entities'][request.GET['entity']] == 'yes':
                modifiedAttributes.append(i['entity'])
                dictOfPolicyDays[i['entity']] = i['duration']
    # print(modifiedAttributes, dictOfPolicyDays)

    dataWithPolicies = {}
    dataWithPolicies['attributes'] = modifiedAttributes
    dataWithPolicies['policy_days'] = dictOfPolicyDays
    # print(dataWithPolicies)
    return JsonResponse(dataWithPolicies)

def deleteHospitalData(request):
    ssn = request.GET['ssn']
    userId = getDataFromDB('./db.sqlite3', 'select id from personal_info where ssn = ' + str(ssn))

    if userId:
        getDataFromDB('./db.sqlite3', 'delete from personal_info where id = ' + str(userId[0][0]))
        getDataFromDB('./hospital_api/Links.db', 'delete from linking where userId = ' + str(ssn))
        getDataFromDB('./hospital_api/policy.db', 'delete from policy where ssn = ' + str(ssn))

        response = requests.get('http://127.0.0.1:8000/diagnosis/deletedg', params = {'id': str(userId[0][0])})
        response = requests.get('http://127.0.0.1:8000/prescription/deletepresc', params = {'id': str(userId[0][0])})
        response = requests.get('http://127.0.0.1:8000/treatment/deletetreatment', params = {'id': str(userId[0][0])})

        response = requests.get('http://127.0.0.1:8000/moh/deletemohdata', params = {'ssn': ssn})

        return HttpResponse("Data deleted from hospital")
    else:
        return HttpResponse("We do not have this person's data to delete")
    
def getPoliciesBasedOnAttributes(request):
    attributes = request.GET.getlist('attributes')
    ssn = request.GET['ssn']
    txid = getDataFromDB('./hospital_api/policy.db', 'select txid from policy where ssn = ' + str(ssn))[0][0]

    rpchost = '127.0.0.1'
    rpcport = '6446'
    rpcuser = 'multichainrpc'
    rpcpassword = 'GJcB9QzPEMzpKb6j4L6SmPCX1Y62jjeXHGXS2xCVpiVF'
    chainname = 'chain1'
    mc = Savoir(rpcuser, rpcpassword, rpchost, rpcport, chainname)

    chainData = mc.liststreamtxitems('stream21', txid)[0]['data']['json']['attributes']

    policy_duration = {}
    for i in attributes:
        for j in chainData:
            if j['entity'] == i:
                policy_duration[i] = j['duration']

    print(attributes, policy_duration)
    return JsonResponse(policy_duration, safe = False)

def definingDefaultPolicies(request):
    rpchost = '127.0.0.1'
    rpcport = '6446'
    rpcuser = 'multichainrpc'
    rpcpassword = 'GJcB9QzPEMzpKb6j4L6SmPCX1Y62jjeXHGXS2xCVpiVF'
    chainname = 'chain1'
    mc = Savoir(rpcuser, rpcpassword, rpchost, rpcport, chainname)

    ssns = getDataFromDB('./db.sqlite3', 'select ssn from personal_info')
    ssns.pop(0)

    f = open('./policy.json')
    data = json.load(f)
    for ssn in ssns:
        data['ssn'] = ssn[0]
        policyToSend = json.loads(json.dumps(data))
        txid = mc.publish("stream21", "key1", {"json" : policyToSend})
        toInsert = (ssn[0], txid)
        updateDatabase('insert into policy(ssn, txid) VALUES(?,?)', './hospital_api/policy.db', toInsert)

    return HttpResponse(200)

def experimentForStorePoliciesOnMultiChain(request):

    rpchost = '127.0.0.1'
    rpcport = '6446'
    rpcuser = 'multichainrpc'
    rpcpassword = 'GJcB9QzPEMzpKb6j4L6SmPCX1Y62jjeXHGXS2xCVpiVF'
    chainname = 'chain1'
    mc = Savoir(rpcuser, rpcpassword, rpchost, rpcport, chainname)

    delay = float(request.GET['delay'])
    noOfRequests = [10, 20, 30, 40, 50, 75, 100]
    f = open('./policy.json')
    data = json.load(f)

    ssns = getDataFromDB('./db.sqlite3', 'select ssn from personal_info')
    ssns.pop(0)

    barTp = {}
    barRAD = {}
    for i in noOfRequests:
        # TP FRT
        tpFirstRequestTime = datetime.now()
        radDifference = 0
        for j in range(i):
            data['ssn'] = ssns[j][0]
            policyToSend = json.loads(json.dumps(data))
            # RAD - req
            radRequestTime = datetime.now()
            time.sleep(delay)
            txid = mc.publish("stream21", "key1", {"json" : policyToSend})
            # RAD - res
            radResponseTime = datetime.now()
            radDifference += (radResponseTime - radRequestTime).total_seconds()
            toInsert = (ssns[j][0], txid)
            updateDatabase('insert into policy(ssn, txid) VALUES(?,?)', './hospital_api/policy.db', toInsert)
        # TP LRT
        radDifference /= i
        print(radDifference)
        barRAD[i] = radDifference
        tpLastRequestTime = datetime.now()
        tpDifference = (tpLastRequestTime - tpFirstRequestTime).total_seconds()
        barTp[i] = i / tpDifference
        
    radY = list(barRAD.values())
    tpY = list(barTp.values())

    fig = plt.figure(figsize = (10, 5))

    plt.bar(['10', '20', '30', '40', '50', '75', '100'], radY, color ='green', width = 0.2)
    
    plt.xlabel("No of Requests")
    plt.ylabel("Resource Access Delay (seconds)")
    plt.title("Resource Access Delay of Storing Policy with " + str(delay) + "s delay")
    plt.savefig("RAD Store Policy with " + str(delay) + "s delay" + ".png")
    plt.clf()

    fig = plt.figure(figsize = (10, 5))

    plt.bar(['10', '20', '30', '40', '50', '75', '100'], tpY, color ='blue', width = 0.2)
    
    plt.xlabel("No of Requests")
    plt.ylabel("Throughput (seconds)")
    plt.title("Throughput of Storing Policy with " + str(delay) + "s delay")
    plt.savefig("TP Store Policy with " + str(delay) + "s delay" + ".png")

    data = {'No of requests': noOfRequests, 'Resource Access Delay': barRAD.values(),'Throughput': barTp.values() }
    df = pd.DataFrame(data)
    df.to_csv("Storing Policy with " + str(delay) + "s delay.csv", index=False)
    return HttpResponse(200)

def callExperiments(request):
    delays = [0, 0.5, 1, 2.5, 5]
    for i in range(5):
        response = requests.get('http://127.0.0.1:8000/datadetails/personal/expolicy', params = {'delay': delays[i]})

    return HttpResponse(200)