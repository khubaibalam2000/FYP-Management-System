import random as rn

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

    return ranges, randRange

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

print(allergens, diagnosis, vital_signs, surgeries, treatments, medicines, immunizations)