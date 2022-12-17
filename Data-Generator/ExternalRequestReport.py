import sqlite3
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def getDataFromDB(dbName, query):
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()
    connection.commit()
    connection.close()
    return rows
    
def exchangedData():
    ssn = 30076841161403

    linkData = getDataFromDB('./Hospital System/main_system/hospital_api/Links.db', 'select * from linking where userId = ' + str(ssn))

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
        exchangers.append(key)
        data.append(values)
    frame = {'Exchanging Entites': exchangers, 'Exchanged Data': data}
    df = pd.DataFrame(frame)

    fig, ax = plt.subplots(figsize=(12,4))
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')

    pp = PdfPages("ExternalExchangedData.pdf")
    pp.savefig(fig, bbox_inches='tight')
    pp.close()
    

def holdingData():
    ssn = 30076841161403
    linkData = getDataFromDB('./Hospital System/main_system/hospital_api/Links.db', 'select * from linking where userId = ' + str(ssn))
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
    for i in externalEntities:
        attributesData.append(getDataFromDB('./Hospital System/main_system/hospital_api/Links.db', 'select attributes from linking where (userId = ' + str(ssn) + ") and (froms = '" + i + "' OR tos = '" + i + "')"))
    
    frame = {'externalEntities': externalEntities, 'attributesData': attributesData}
    df = pd.DataFrame(frame)
    
    fig, ax = plt.subplots(figsize=(12,4))
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')

    pp = PdfPages("HoldingDataEntities.pdf")
    pp.savefig(fig, bbox_inches='tight')
    pp.close()

exchangedData()
holdingData()