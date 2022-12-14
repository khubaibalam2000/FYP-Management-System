import plotly.express as px
import sqlite3
import random as rn
import pandas as pd

def getDataFromDB(dbName, query):
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()
    connection.commit()
    connection.close()
    return rows

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

userId = rn.randint(0, 1000)

pii = getDataFromDB('./Data-Files/DB-Files/piiDb.db', 'select * from personal_info where id = ' + str(userId))
diagnosis = getDataFromDB('./Data-Files/DB-Files/diagnosisDb.db', 'select * from diagnosis where id = ' + str(userId))
labreps = getDataFromDB('./Data-Files/DB-Files/labReps.db', 'select * from lab_reports where id = ' + str(userId))
medicines = getDataFromDB('./Data-Files/DB-Files/prescriptionsDb.db', 'select * from medicines where id = ' + str(userId))
habits = getDataFromDB('./Data-Files/DB-Files/habitsDb.db', 'select * from habits where id = ' + str(userId))
allergens = getDataFromDB('./Data-Files/DB-Files/allergyDb.db', 'select * from allergies where id = ' + str(userId))
vs = getDataFromDB('./Data-Files/DB-Files/vitalSignsDb.db', 'select * from vital_signs where id = ' + str(userId))
treats = getDataFromDB('./Data-Files/DB-Files/treatmentsDb.db', 'select * from treatments where id = ' + str(userId))
surgeries = getDataFromDB('./Data-Files/DB-Files/surgeryDb.db', 'select * from surgeries where id = ' + str(userId))
immunizations = getDataFromDB('./Data-Files/DB-Files/immunizationsDb.db', 'select * from immunizations where id = ' + str(userId))

dictForUser = makeDataFrameForUser(pii, diagnosis, medicines, habits, allergens, vs, treats, surgeries, immunizations)
df = pd.DataFrame(dictForUser)

fig = px.scatter(df, x="entity", y="y", color="entity", size='size', hover_data={'x':False, 'y':False, 'entity':True, 'size': False, 'data':True})
fig.show()