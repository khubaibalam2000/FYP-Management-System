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

def getRandomDate(dateList):
    d1 = datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('1/1/2022 4:50 AM', '%m/%d/%Y %I:%M %p')
    for i in range(1000):
        temp = (random_date(d1, d2))
        dateList.append(temp)

def sendDataToCSV(path, data):
    df = pd.DataFrame(data)
    df.to_csv(path)

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
    df.to_csv('./Data-Files/Habits.csv')

# def randomVitalSigns():
#     for i in range(1000):

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
# csvVitalSigns = makeRandomValues(vital_signs, 3, len(vital_signs) - 1)
csvSurgeries = makeRandomValues(surgeries, 2, len(surgeries) - 1)
csvTreatments = makeRandomValues(treatments, 3, len(treatments) - 1)
csvMedicines = makeRandomValues(medicines, 15, len(medicines) - 1)
csvImmunizations = makeRandomValues(immunizations, 2, len(immunizations) - 1)

dateForDiagnosis = []
dateForSurgeries = []
dateForTreatments = []
dateForMedicines = []
dateForImmunizations = []

getRandomDate(dateForDiagnosis)
getRandomDate(dateForSurgeries)
getRandomDate(dateForTreatments)
getRandomDate(dateForMedicines)
getRandomDate(dateForImmunizations)

sendDataToCSV('./Data-Files/Allergens.csv', {'Diagnosis': csvAllergens})
sendDataToCSV('./Data-Files/Diagnosis.csv', {'Diagnosis': csvDiagnosis, 'Date of Diagnosis': dateForDiagnosis})
# sendDataToCSV('./Data-Files/Diagnosis.csv', {'Diagnosis': csvDiagnosis, 'Date of Diagnosis': dateForDiagnosis})
sendDataToCSV('./Data-Files/Surgeries.csv', {'Diagnosis': csvSurgeries, 'Date of Diagnosis': dateForSurgeries})
sendDataToCSV('./Data-Files/Treatments.csv', {'Diagnosis': csvTreatments, 'Date of Diagnosis': dateForTreatments})
sendDataToCSV('./Data-Files/Medicines.csv', {'Diagnosis': csvMedicines, 'Date of Diagnosis': dateForMedicines})
sendDataToCSV('./Data-Files/Immunizations.csv', {'Diagnosis': csvImmunizations, 'Date of Diagnosis': dateForImmunizations})
generateHabits()