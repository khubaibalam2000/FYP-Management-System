import random as rn
import pandas as pd
from random import randrange
from datetime import timedelta
from datetime import datetime

def readFile(fileName, listToStore):
    with open(fileName) as stream:
        for line in stream:
            if line.strip():
                line = line.replace('\n', '')
                listToStore.append(line)

def getRange(totalTerms, totalData):
    ranges = rn.randint(0,totalTerms)
    randRange = []
    i = 0
    while i < ranges:
        found = rn.randint(0, totalData)
        if found not in randRange:
            randRange.append(found)
            i+=1

    return randRange

def makeRandomValues(data, totalTerms, totalData):
    finalData = []
    for i in range(1000):
        ranger = getRange(totalTerms, totalData)
        tempData = []
        for j in range(len(ranger)):
            tempData.append(data[ranger[j]])
        finalData.append(tempData)
    return finalData


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def sendDataToCSV(path, data):
    df = pd.DataFrame(data)
    df.to_csv(path, header=False, index=False)

def generateHabits():
    alcoholic = []
    smoker = []
    veg = []
    beverages = []
    exercise = []
    for i in range(1000):
        alcoholic.append(rn.randint(0,1))
        smoker.append(rn.randint(0,1))
        veg.append(rn.randint(0,1))
        beverages.append(rn.randint(0,1))
        exercise.append(rn.randint(0,1))
    dictForHabits = {'Alcoholic': alcoholic, 'Smoker': smoker, 'Veg': veg, 'Soft Drinks': beverages, 'Exercise': exercise}
    df = pd.DataFrame(dictForHabits)
    df.to_csv('./Data-Files/CSV-Files/Habits.csv', header=False, index=False)

def randomVitalSigns():
    hr = []
    bp = []
    rr = []
    spo2 = []
    temperature = []
    for i in range(1000):
        hr.append(rn.randint(50,115))
        bp.append(rn.randint(70,140))
        rr.append(rn.randint(8,22))
        spo2.append(rn.randint(90,100))
        temperature.append(rn.randint(97,104))
    dictForVS = {'Heart Rate': hr, 'Blood Pressure': bp, 'Respiration Rate': rr, 'Oxygen Saturation': spo2, 'Temperature': temperature}
    df = pd.DataFrame(dictForVS)
    df.to_csv('./Data-Files/CSV-Files/VitalSigns.csv', header=False, index=False) 

allergens = []
diagnosis = []
vital_signs = []
surgeries = []
treatments = []
medicines = []
immunizations = []

readFile('./Data-Files/Temp-Data/TempAllergens.txt', allergens)
readFile('./Data-Files/Temp-Data/TempDiagnosis.txt', diagnosis)
readFile('./Data-Files/Temp-Data/TempVitalSigns.txt', vital_signs)
readFile('./Data-Files/Temp-Data/TempSurgeries.txt', surgeries)
readFile('./Data-Files/Temp-Data/TempTreatments.txt', treatments)
readFile('./Data-Files/Temp-Data/TempMedicines.txt', medicines)
readFile('./Data-Files/Temp-Data/TempImmunizations.txt', immunizations)

csvAllergens = makeRandomValues(allergens, 4, len(allergens) - 1)
csvDiagnosis = makeRandomValues(diagnosis, 3, len(diagnosis) - 1)
csvSurgeries = makeRandomValues(surgeries, 2, len(surgeries) - 1)
csvTreatments = makeRandomValues(treatments, 3, len(treatments) - 1)
csvMedicines = makeRandomValues(medicines, 8, len(medicines) - 1)
csvImmunizations = makeRandomValues(immunizations, 2, len(immunizations) - 1)

sendDataToCSV('./Data-Files/CSV-Files/Allergens.csv', {'Allergens': csvAllergens})
sendDataToCSV('./Data-Files/CSV-Files/Diagnosis.csv', {'Diagnosis': csvDiagnosis})
# sendDataToCSV('./Data-Files/CSV-Files/Diagnosis.csv', {'Diagnosis': csvDiagnosis, 'Date of Diagnosis': dateForDiagnosis})
sendDataToCSV('./Data-Files/CSV-Files/Surgeries.csv', {'Surgeries': csvSurgeries})
sendDataToCSV('./Data-Files/CSV-Files/Treatments.csv', {'Treatments': csvTreatments})
sendDataToCSV('./Data-Files/CSV-Files/Medicines.csv', {'Medicines': csvMedicines})
sendDataToCSV('./Data-Files/CSV-Files/Immunizations.csv', {'Immunizations': csvImmunizations})
generateHabits()
randomVitalSigns()