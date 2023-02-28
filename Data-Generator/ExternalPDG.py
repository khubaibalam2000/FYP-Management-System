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
#                 ''', './Hospital System/main_system/paramedics/Linkspara.db')


# createLinkingDatabase('''CREATE TABLE data(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 ssn INTEGER,
#                 data TEXT,
#                 policy TEXT,
#                 received_at TEXT);
#                 ''', './Hospital System/main_system/paramedics/datas.db')

# createLinkingDatabase('''CREATE TABLE data(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 ssn INTEGER,
#                 data TEXT);
#                 ''', './Hospital System/main_system/paramedics/datas.db')

# createLinkingDatabase('''CREATE TABLE policy(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 ssn INTEGER,
#                 txid TEXT);
#                 ''', './Hospital System/main_system/hospital_api/policy.db')

def getDataFromDB(dbName, query):
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()
    connection.commit()
    connection.close()
    return rows

# 30076841161403
# getDataFromDB('./Hospital System/main_system/hospital_api/Links.db', "delete from linking where userId = 30076841161403")
# getDataFromDB('./Hospital System/main_system/paramedics/datas.db', "drop table data")
# getDataFromDB('./Hospital System/main_system/ministry_of_health/datas.db', "delete from data where ssn = 4903773748744614")
# getDataFromDB('./Hospital System/main_system/db.sqlite3', "insert into personal_info (id, name, DOB, city, province, gender, email, phone, ssn) values (18, 'abeer hussain', '2/3/1992', 'karachi', 'SI', 'Male', 'disoc.kutta@gmail.com', '0317 232 2323', '4903773748744614')")

def drawExternalPDGWithConnections():
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
    plt.show()

def drawExternalPDGWithoutConnections():
    ssn = 30076841161403
    linkData = getDataFromDB('./Hospital System/main_system/hospital_api/Links.db', 'select * from linking where userId = ' + str(ssn))
    print(linkData)
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
    print(dictForData)
    externalEntities = []
    for key, value in dictForData.items():
        externalEntities.append(key[0])
        externalEntities.append(key[1])
    externalEntities = list(set(externalEntities))
    attributesData = []
    for i in externalEntities:
        attributesData.append(getDataFromDB('./Hospital System/main_system/hospital_api/Links.db', 'select attributes from linking where (userId = ' + str(ssn) + ") and (froms = '" + i + "' OR tos = '" + i + "')"))
    
    frame = {'x': x, 'y': y, 'externalEntities': externalEntities, 'attributesData': attributesData}
    print(frame)
    df = pd.DataFrame(frame)
    fig = px.scatter(df, x="x", y="y", color="externalEntities", hover_data={'x': False, 'y': False, 'externalEntities':True, 'attributesData':True})
    fig.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
    fig.show()

# drawExternalPDGWithConnections()
# drawExternalPDGWithoutConnections()