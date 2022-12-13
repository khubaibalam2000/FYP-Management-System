import networkx as nx
import matplotlib.pyplot as plt
import sqlite3
import random as rn
import pandas as pd
import plotly.express as px

def createLinkingDatabase(queryCreation, dbPath):
    connection = sqlite3.connect(dbPath)
    cursor = connection.cursor()
    cursor.execute(queryCreation)
    connection.commit()
    connection.close()

# createLinkingDatabase('''CREATE TABLE linking(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 userId INTEGER,
#                 attributes TEXT,
#                 froms TEXT,
#                 tos TEXT);
#                 ''', './Hospital System/main_system/hospital_api/Links.db')

def getDataFromDB(dbName, query):
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()
    connection.commit()
    connection.close()
    return rows

def drawExternalPDGWithConnections():
    ssn = 4903773748744614

    linkData = getDataFromDB('./Hospital System/main_system/hospital_api/Links.db', 'select * from linking where userId = ' + str(ssn))

    dictForData = {}
    for i in linkData:
        if (i[3][2:len(i[3])-2], i[4][2:len(i[4])-2]) in dictForData:
            a = dictForData[(i[3][2:len(i[3])-2], i[4][2:len(i[4])-2])]
            a += i[2]
            dictForData[(i[3][2:len(i[3])-2], i[4][2:len(i[4])-2])] = a
            continue
        dictForData[(i[3][2:len(i[3])-2], i[4][2:len(i[4])-2])] = i[2]

    E = []
    pos = {}
    for key, values in dictForData.items():
        E.append((key[0], key[1], values))
        pos[key[0]] = [rn.randint(0,10), rn.randint(0,10)]
        pos[key[1]] = [rn.randint(0,10), rn.randint(0,10)]
    G = nx.DiGraph()
    G.add_weighted_edges_from(E)
    weight = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos=pos, with_labels=True, node_size=1000, node_color='r', edge_color='g', arrowsize=35)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weight)
    plt.figure()
    plt.show()

def drawExternalPDGWithoutConnections():
    ssn = 4903773748744614
    linkData = getDataFromDB('./Hospital System/main_system/hospital_api/Links.db', 'select * from linking where userId = ' + str(ssn))
    print(linkData)
    x = []
    y = []
    for i in range(3): x.append(rn.randint(0,6))
    for i in range(3): y.append(rn.randint(0,6))

    dictForData = {}
    for i in linkData:
        if (i[3][2:len(i[3])-2], i[4][2:len(i[4])-2]) in dictForData:
            a = dictForData[(i[3], i[4])]
            a += i[2]
            dictForData[(i[3], i[4])] = a
            continue
        dictForData[(i[3], i[4])] = i[2]
    print(dictForData)
    externalEntities = []
    for key, value in dictForData.items():
        externalEntities.append(key[0])
        externalEntities.append(key[1])
    externalEntities = list(set(externalEntities))
    print(externalEntities)
    attributesData = []
    for i in externalEntities:
        attributesData.append(getDataFromDB('./Hospital System/main_system/hospital_api/Links.db', 'select attributes from linking where (userId = ' + str(ssn) + ") and (froms = '" + i + "' OR tos = '" + i + "')"))
    
    # attributesData = list(set(attributesData))
    print(attributesData)

    # select attributes from linking where userId = 4903773748744614 and froms = Paramedics and tos = Paramedics
    # fig = px.scatter(dictForData, x="x", y="y", color="entity", hover_data={'x':False, 'y':False, 'entity':True, 'size': False, 'data':True})
    # fig.show()

# drawExternalPDGWithConnections()
drawExternalPDGWithoutConnections()