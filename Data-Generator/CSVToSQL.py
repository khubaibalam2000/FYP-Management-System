import csv
import sqlite3


def createTable(queryCreation, csvPath, queryInsertion, dbPath):
    connection = sqlite3.connect(dbPath)
    cursor = connection.cursor()
    cursor.execute(queryCreation)
    file = open(csvPath)
    contents = csv.reader(file)
    cursor.executemany(queryInsertion, contents)
    connection.commit()
    connection.close()

createTable('''CREATE TABLE allergies(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                allergen TEXT);
                ''', './Data-Files/CSV-Files/Allergens.csv', 'INSERT INTO allergies(allergen) VALUES(?)', './Data-Files/DB-Files/allergyDb.db')

createTable('''CREATE TABLE diagnosis(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                diagnose TEXT);
                ''', './Data-Files/CSV-Files/Diagnosis.csv', 'INSERT INTO diagnosis(diagnose) VALUES(?)', './Data-Files/DB-Files/diagnosisDb.db')

createTable('''CREATE TABLE surgeries(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                surgery TEXT);
                ''', './Data-Files/CSV-Files/Surgeries.csv', 'INSERT INTO surgeries(surgery) VALUES(?)', './Data-Files/DB-Files/surgeryDb.db')

createTable('''CREATE TABLE treatments(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                treatment TEXT);
                ''', './Data-Files/CSV-Files/Treatments.csv', 'INSERT INTO treatments(treatment) VALUES(?)', './Data-Files/DB-Files/treatmentsDb.db')

createTable('''CREATE TABLE medicines(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medicine TEXT);
                ''', './Data-Files/CSV-Files/Medicines.csv', 'INSERT INTO medicines(medicine) VALUES(?)', './Data-Files/DB-Files/prescriptionsDb.db')

createTable('''CREATE TABLE immunizations(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                immunization TEXT);
                ''', './Data-Files/CSV-Files/Immunizations.csv', 'INSERT INTO immunizations(immunization) VALUES(?)', './Data-Files/DB-Files/immunizationsDb.db')

createTable('''CREATE TABLE habits(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alcoholic TEXT,
                smoker TEXT,
                veg TEXT,
                soft_drink TEXT,
                exercise TEXT);
                ''', './Data-Files/CSV-Files/Habits.csv', 'INSERT INTO habits(alcoholic, smoker, veg, soft_drink, exercise) VALUES(?,?,?,?,?)', './Data-Files/DB-Files/habitsDb.db')

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
                ''', './Data-Files/CSV-Files/PII-data.csv', 'INSERT INTO personal_info(name, DOB, city, province, gender, email, phone, ssn) VALUES(?,?,?,?,?,?,?,?)', './Data-Files/DB-Files/piiDb.db')

createTable('''CREATE TABLE lab_reports(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Albumin_g_dL TEXT,
                Albumin_g_L TEXT,
                Alanine_aminotransferase_ALT_U_L TEXT,
                Aspartate_aminotransferase_AST_U_L TEXT,
                Alkaline_phosphotase_U_L TEXT,
                Blood_urea_nitrogen_mg_dL TEXT,
                Blood_urea_nitrogen_mmol_L TEXT,
                Total_calcium_mg_dL TEXT,
                Total_calcium_mmol_L TEXT,
                Creatine_Phosphokinase_CPK_IU_L TEXT,
                Cholesterol_mg_dL TEXT,
                Cholesterol_mmol_L TEXT,
                Bicarbonate_mmol_L TEXT,
                Creatinine_mgdL TEXT,
                Creatinine_umol_L TEXT,
                Gamma_glutamyl_transferase_U_L TEXT,
                Glucose_serum_mg_dL TEXT,
                Glucose_serum_mmol_L TEXT,
                Iron_refigerated_ug_dL TEXT,
                Iron_refigerated_umol_L TEXT,
                Lactate_dehydrogenase_U_L TEXT,
                Phosphorus_mg_dL TEXT,
                Phosphorus_mmol_L TEXT,
                Total_bilirubin_mg_dL TEXT,
                Total_bilirubin_umol_L TEXT,
                Total_protein_g_dL TEXT,
                Total_protein_g_L TEXT,
                Uric_acid_mg_dL TEXT,
                Uric_acid_umol_L TEXT,
                Sodium_mmol_L TEXT,
                Potassium_mmol_L TEXT,
                Chloride_mmol_L TEXT,
                Osmolality_mmol_Kg TEXT,
                Globulin_g_dL TEXT,
                Globulin_g_L TEXT,
                Triglycerides_mg_dL TEXT,
                Triglycerides_mmol_L TEXT);
                ''', './Data-Files/CSV-Files/BIOPRO_G.csv', 'INSERT INTO lab_reports(Albumin_g_dL,Albumin_g_L,Alanine_aminotransferase_ALT_U_L,Aspartate_aminotransferase_AST_U_L,Alkaline_phosphotase_U_L,Blood_urea_nitrogen_mg_dL,Blood_urea_nitrogen_mmol_L,Total_calcium_mg_dL,Total_calcium_mmol_L,Creatine_Phosphokinase_CPK_IU_L,Cholesterol_mg_dL,Cholesterol_mmol_L,Bicarbonate_mmol_L,Creatinine_mgdL,Creatinine_umol_L,Gamma_glutamyl_transferase_U_L,Glucose_serum_mg_dL,Glucose_serum_mmol_L,Iron_refigerated_ug_dL,Iron_refigerated_umol_L,Lactate_dehydrogenase_U_L,Phosphorus_mg_dL,Phosphorus_mmol_L,Total_bilirubin_mg_dL,Total_bilirubin_umol_L,Total_protein_g_dL,Total_protein_g_L,Uric_acid_mg_dL,Uric_acid_umol_L,Sodium_mmol_L,Potassium_mmol_L,Chloride_mmol_L,Osmolality_mmol_Kg,Globulin_g_dL,Globulin_g_L,Triglycerides_mg_dL,Triglycerides_mmol_L) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', './Data-Files/DB-Files/labReps.db')

createTable('''CREATE TABLE vital_signs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Heart_Rate TEXT,
                Blood_Pressure TEXT,
                Respiration_Rate TEXT,
                Oxygen_Saturation TEXT,
                Temperature TEXT);
                ''', './Data-Files/CSV-Files/VitalSigns.csv', 'INSERT INTO vital_signs(Heart_Rate, Blood_Pressure, Respiration_Rate, Oxygen_Saturation, Temperature) VALUES(?,?,?,?,?)', './Data-Files/DB-Files/vitalSignsDb.db')