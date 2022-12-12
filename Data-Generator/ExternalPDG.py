import networkx as nx
import matplotlib.pyplot as plt
import sqlite3
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
#                 ''', './Data-Files/DB-Files/Links.db')

def getDataFromDB(dbName, query):
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()
    connection.commit()
    connection.close()
    return rows


ssn = 4903773748744614

linkData = getDataFromDB('./Data-Files/DB-Files/Links.db', 'select * from linking where userId = ' + str(ssn))
edges = []
G = nx.DiGraph()
# G.add_node('H')
# G.add_node('MH')
# G.add_node('P')
for i in linkData:
    G.add_edge(i[3][2:len(i[3])-2], i[4][2:len(i[4])-2], weight=5)
    # edges.append((i[3][2:len(i[3])-2], i[4][2:len(i[4])-2]))
# G.add_edges_from(edges)
# print(linkData[0][1])
# dict = {
#     'Hospital':1,'MinistryOfHealth':2,'Paramedics':3
# }
# dict = {0: {'attr1': 20, 'attr2': 'nothing'}, 1: {'attr2': 3}, 2: {'attr1': 42}, 3: {'attr3': 'hello'}, 4: {'attr1': 54, 'attr3': '33'}}
# nx.set_node_attributes(G, values=(dict))
# plt.figure(figsize =(9, 9))
# nx.draw_networkx(G, with_labels=True, node_color ='green')


plt.figure()    
pos = nx.spring_layout(G)
weight_labels = nx.get_edge_attributes(G,'weight')
nx.draw(G,pos,font_color = 'white', node_shape = 's', with_labels = True,)
output = nx.draw_networkx_edge_labels(G,pos,edge_labels=weight_labels)
plt.show()

# plt.show()
# plt.savefig("UserGraph.png")