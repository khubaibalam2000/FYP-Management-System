import csv
import sqlite3

connection = sqlite3.connect('./Data-Files/Data.db')
cursor = connection.cursor()

def createTable(queryCreation, csvPath, queryInsertion):
    cursor.execute(queryCreation)
    file = open(csvPath)
    contents = csv.reader(file)
    cursor.executemany(queryInsertion, contents)

createTable('''CREATE TABLE allergies(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                allergen TEXT);
                ''', './Data-Files/CSV-Files/Allergens.csv', 'INSERT INTO allergies(allergen) VALUES(?)')

createTable('''CREATE TABLE diagnosis(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                diagnose TEXT);
                ''', './Data-Files/CSV-Files/Diagnosis.csv', 'INSERT INTO diagnosis(diagnose) VALUES(?)')

createTable('''CREATE TABLE surgeries(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                surgery TEXT);
                ''', './Data-Files/CSV-Files/Surgeries.csv', 'INSERT INTO surgeries(surgery) VALUES(?)')

createTable('''CREATE TABLE treatments(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                treatment TEXT);
                ''', './Data-Files/CSV-Files/Treatments.csv', 'INSERT INTO treatments(treatment) VALUES(?)')

createTable('''CREATE TABLE medicines(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medicine TEXT);
                ''', './Data-Files/CSV-Files/Medicines.csv', 'INSERT INTO medicines(medicine) VALUES(?)')

createTable('''CREATE TABLE immunizations(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                immunization TEXT);
                ''', './Data-Files/CSV-Files/Immunizations.csv', 'INSERT INTO immunizations(immunization) VALUES(?)')

createTable('''CREATE TABLE habits(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alcoholic TEXT,
                smoker TEXT,
                veg TEXT,
                soft_drink TEXT,
                exercise TEXT);
                ''', './Data-Files/CSV-Files/Habits.csv', 'INSERT INTO habits(alcoholic, smoker, veg, soft_drink, exercise) VALUES(?,?,?,?,?)')

createTable('''CREATE TABLE personal_info(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                DOB TEXT,
                city TEXT,
                province TEXT,
                gender TEXT,
                email TEXT,
                phone TEXT,
                ssn TEXT);
                ''', './Data-Files/CSV-Files/PII-data.csv', 'INSERT INTO personal_info(name, DOB, city, province, gender, email, phone, ssn) VALUES(?,?,?,?,?,?,?,?)')

connection.commit()
connection.close()