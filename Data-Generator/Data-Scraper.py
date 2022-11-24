# Importing Libraries
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pandas as pd

# Lists of data
allergens = ['Balsam of Peru', 'Buckwheat', 'Celery', 'Egg', 'Fish', 'Fruit', 'Garlic', 'Oats', 'Maize', 'Milk', 'Mustard', 'Peanut', 'Poultry Meat', 'Rice', 'Sesame', 'Shellfish', 'Soy', 'Sulfites', 'Tartrazine', 'Tree nut', 'Wheat', 'Balsam of Peru', 'Tetracycline', 'Dilantin', 'Tegretol', 'Penicillin', 'Cephalosporins', 'Sulfonamides', 'Non-steroidal anti-inflammatories', 'Intravenous contrast dye', 'Local anesthetics', 'Balsam of Peru', 'Pollen', 'Cat', 'Dog', 'Insect sting', 'Mold', 'Perfume', 'Cosmetics', 'Latex', 'Water', 'Cold stimuli', 'House dust mite', 'Nickel', 'Gold', 'Chromium', 'Cobalt', 'Formaldehyde', 'Photographic developers', 'Fungicide']
diagnosis = []
vitals_signs = ['body temperature', 'pulse', 'respiration rate', 'BP', 'SpO2']
surgeries = []
treatments = []
immunizations = ['Cholera', 'COVID-19 (corona virus)', 'Dengue', 'Diphtheria', 'Hepatitis', 'Haemophilus influenzae type b (Hib)', 'Human papillomavirus (HPV)', 'Influenza', 'Japanese encephalitis', 'Malaria', 'Measles', 'Meningococcal meningitis', 'Mumps', 'Pertussis', 'Pneumococcal disease', 'Poliomyelitis', 'Rabies', 'Rotavirus', 'Rubella', 'Tetanus', 'Tick-borne encephalitis', 'Tuberculosis', 'Typhoid', 'Varicella', 'Yellow Fever', 'Enterotoxigenic Escherichia coli', 'Group B Streptococcus (GBS)', 'Herpes Simplex Virus', 'HIV-1''Malaria', 'Neisseria gonorrhoeae', 'Nontyphoidal Salmonella Disease', 'Norovirus', 'Paratyphoid fever', 'Respiratory Syncytial Virus (RSV)', 'Schistosomiasis Disease', 'Shigella', 'Group A Streptococcus (GAS)', 'Tuberculosis', 'Improved Influenza Vaccines']
medicines = []

# Diagnosis Scraping
url = "https://dph.illinois.gov/topics-services/diseases-and-conditions/diseases-a-z-list.html"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
abc = (soup.find_all('p'))
for i in abc:
    diagnosis.append(i.text)
diagnosis.pop(0)


# surgeries Scraping
url = "https://en.wikipedia.org/wiki/List_of_surgical_procedures"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
abc = soup.find_all('td')
tempSurgeryForTables = []
for i in abc:
    tempSurgeryForTables.append(i.text)

for i in tempSurgeryForTables:
    tempSurgeryForInsideTables = i.split('\xa0')
    for j in tempSurgeryForInsideTables:
        j = j.replace('\n', '')
        j = j.replace('· ', '')
        surgeries.append(j)
surgeries.remove('·')

# treatments Scraping
url = "https://en.wikipedia.org/wiki/Category:Medical_treatments"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
abc = soup.find_all('a')
for i in abc:
    treatments.append(i.text)
for i in range(33):
    treatments.pop(0)
for i in range(128):
    treatments.pop()

# Medicines Scraping
url = "https://www.nhs.uk/medicines/"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
abc = soup.find_all('a')
for i in abc:
    tempMeds = i.text
    tempMeds = tempMeds.replace(' ', '')
    tempMeds = tempMeds.replace('\n', '')
    medicines.append(tempMeds)
for i in range(34):
    medicines.pop(0)
for i in range(21):
    medicines.pop()

# Writing into files for further processing
def writeToFile(path, data):
    with open(path, 'w') as fp:
        for item in data:
            fp.write("%s\n" % item)

writeToFile('./Data-Files/Temp-Data/TempAllergens.txt', allergens)
writeToFile('./Data-Files/Temp-Data/TempDiagnosis.txt', diagnosis)
writeToFile('./Data-Files/Temp-Data/TempVitalSigns.txt', vitals_signs)
writeToFile('./Data-Files/Temp-Data/TempSurgeries.txt', surgeries)
writeToFile('./Data-Files/Temp-Data/TempTreatments.txt', treatments)
writeToFile('./Data-Files/Temp-Data/TempImmunizations.txt', immunizations)
writeToFile('./Data-Files/Temp-Data/TempMedicines.txt', medicines)