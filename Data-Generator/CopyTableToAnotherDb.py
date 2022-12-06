from sqlite3 import connect
from sys import argv

def CopyTable():
    newdb = argv[1]
    olddb = argv[2]
    tablename = argv[3]

    conn = connect(newdb)
    cursor = conn.cursor()
    cursor.execute("ATTACH DATABASE '"+ olddb +"' AS new_db;")
    query = "CREATE TABLE "+ tablename + " AS SELECT * FROM new_db."+ tablename +";"
    cursor.execute(query)

    conn.commit()
    conn.close()



if __name__ == "__main__":
    CopyTable()

    #python CopyTableToAnotherDb.py piiDb.db vitalSignsDb.db vital_signs
