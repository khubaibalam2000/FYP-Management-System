import sqlite3
import random as rn
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Table
from reportlab.platypus import Spacer, Paragraph

def getDataFromDB(dbName, query):
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()
    connection.commit()
    connection.close()
    return rows

listPii, listDiag, listMeds, listHabits, listAllergens, listVS, listTreats, listSurgery, listImmuns = [], [], [], [], [], [], [], [], []
def organizeDataForReport(pii, diagnosis, medicines, habits, allergens, vs, treats, surgeries, immunizations):
    listPii.append(['id', 'name', 'DOB', 'city', 'province', 'gender', 'email', 'phone', 'ssn'])
    listPii.append(list(pii[0]))

    listDiag.append(['id', 'diagnose'])
    listDiag.append(list(diagnosis[0]))

    listMeds.append(['id', 'medicines'])
    listMeds.append(list(medicines[0]))

    listHabits.append(['id', 'alcoholic', 'smoker', 'veg', 'soft_drink', 'exercise'])
    listHabits.append(list(habits[0]))

    listAllergens.append(['id', 'allergens'])
    listAllergens.append(list(allergens[0]))

    listVS.append(['id', 'Heart_Rate', 'Blood_Pressure', 'Respiration_Rate', 'Oxygen_Saturation', 'Temperature'])
    listVS.append(list(vs[0]))

    listTreats.append(['id', 'treatments'])
    listTreats.append(list(treats[0]))

    listSurgery.append(['id', 'surgery'])
    listSurgery.append(list(surgeries[0]))

    listImmuns.append(['id', 'immuns'])
    listImmuns.append(list(immunizations[0]))

elems = []
fileName = 'ReportSummary.pdf'
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


userId = rn.randint(0,1000)

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

organizeDataForReport(pii, diagnosis, medicines, habits, allergens, vs, treats, surgeries, immunizations)
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
# elems.append(Spacer(20,40))
p = Paragraph('Prescriptions Departmnet', 
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
p = Paragraph('Habits', 
    ParagraphStyle('okay', fontName='Helvetica', fontSize=15)
)
elems.append(p)
elems.append(Spacer(20,10))
generateReportSummary(listHabits)
p = Paragraph('Allergens', 
    ParagraphStyle('okay', fontName='Helvetica', fontSize=15)
)
elems.append(p)
elems.append(Spacer(20,10))
generateReportSummary(listAllergens)
p = Paragraph('Vital Signs Data', 
    ParagraphStyle('okay', fontName='Helvetica', fontSize=15)
)
elems.append(p)
elems.append(Spacer(20,10))
generateReportSummary(listVS)
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
p = Paragraph('Surgeries', 
    ParagraphStyle('okay', fontName='Helvetica', fontSize=15)
)
elems.append(p)
elems.append(Spacer(20,10))
generateReportSummary(listSurgery)
p = Paragraph('Immunizations', 
    ParagraphStyle('okay', fontName='Helvetica', fontSize=15)
)
elems.append(p)
elems.append(Spacer(20,10))
generateReportSummary(listImmuns)
pdf.build(elems)