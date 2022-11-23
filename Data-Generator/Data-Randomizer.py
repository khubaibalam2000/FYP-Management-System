import random as rn
import pandas as pd
from random import randrange
from datetime import timedelta

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


def makeRandomValues(data, totalTerms, totalData):
    finalData = []
    for i in range(1000):
        ranger = getRange(totalTerms, totalData)
        tempData = []
        for j in range(len(ranger)):
            tempData.append(data[ranger[j]])
        finalData.append(tempData)
    return finalData


# def randomVitalSigns():
#     for i in range(1000):

        

csvAllergens = makeRandomValues(allergens, 4, len(allergens) - 1)
csvDiagnosis = makeRandomValues(diagnosis, 3, len(diagnosis) - 1)
# csvVitalSigns = makeRandomValues(vital_signs, 3, len(vital_signs) - 1)
csvSurgeries = makeRandomValues(surgeries, 2, len(surgeries) - 1)
csvTreatments = makeRandomValues(treatments, 3, len(treatments) - 1)
csvMedicines = makeRandomValues(medicines, 15, len(medicines) - 1)
csvImmunizations = makeRandomValues(immunizations, 2, len(immunizations) - 1)

