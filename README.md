# FYP-Management-System

PrivacyOps in Smart Cities, FYP code repository.

# How to run:

1. Clone the Repository
2. Go to the folder ./FYP-Management-System
3. Run "pip install -r requirements.txt"
4. Switch to 'PDG-and-Reports' branch.
5. Go the ./FYP-Management-System/Hospital System/main_system, and then run 'python manage.py runserver'.

# How to Merge Tables into db:
```
    python CopyTableToAnotherDb.py (Name of db to add table) (Name of db to add table from) (table name)
```

cd "Hospital System/main_system"

# APIs to Call:
## 1. /datadetails/personal/requestForData in hospital_api (GET API: gets json):
    Function: Gets the required data from internal systems of hospital.
    parameters: ssn, froms, tos, attributes (attributes parameter can be passed multiple times)
    Example Link:
    http://127.0.0.1:8000/datadetails/personal/requestForData/?ssn=4903773748744614&froms=Hospital&tos=Paramedics&attributes=name&attributes=city&attributes=province
    http://127.0.0.1:8000/datadetails/personal/requestForData/?ssn=4903773748744614&froms=Hospital&tos=MinistryOfHealth&attributes=name&attributes=province
    
## 2. /datadetails/personal/inform in hospital_api (GET API: gets json):
    Function: Ministry Of Health informs the hospital what attributes they shared if they share the data to some external entity.
    parameters: ssn, froms, tos, attributes (attributes parameter can be passed multiple times)
    Example Link:
    http://127.0.0.1:8000/datadetails/personal/inform/?ssn=4903773748744614&froms=Hospital&tos=Paramedics&attributes=name&attributes=city&attributes=province
    http://127.0.0.1:8000/datadetails/personal/inform/?ssn=4903773748744614&froms=Hospital&tos=MinistryOfHealth&attributes=name&attributes=province
    
## 3. /datadetails/personal/epdgwithconnection (GET API: gets image png):
    Function: Generate external people data graph with connections explaining that which data is shared among external entities of given SSN id.
    parameters: ssn
    Example Link:
    http://127.0.0.1:8000/datadetails/personal/epdgwithconnection/?ssn=4903773748744614
    
## 4. /datadetails/personal/epdgwithoutconnection (GET API: gets .html file):
    Function: Generate external people data graph without connections explaining that which entity stores what data of given SSN id.
    parameters: ssn
    Example Link:
    http://127.0.0.1:8000/datadetails/personal/epdgwithoutconnection/?ssn=4903773748744614
    
## 5. /datadetails/personal/ipdg (GET API: gets .html file):
    Function: Generate Internal people data graph explaining what data stores in the hospital and its internal departments given user id.
    parameters: id
    Example Link:
    http://127.0.0.1:8000/datadetails/personal/ipdg/?id=400
    
## 6. /datadetails/personal/eXdataReport (GET API: gets .pdf file):
    Function: Generate report explaining that what data exchanged among different external entities.
    parameters: ssn
    Example Link:
    http://127.0.0.1:8000/datadetails/personal/eXdataReport/?ssn=4903773748744614
    
## 7. /datadetails/personal/eHdataReport (GET API: gets .pdf file):
    Function: Generate report explaining that which entity holds what data of the user.
    parameters: ssn
    Example Link:
    http://127.0.0.1:8000/datadetails/personal/eHdataReport/?ssn=4903773748744614
    
## 8. /datadetails/personal/ireport (GET API: gets .pdf file):
    Function: Generate report by extracting all the data from hospital and its internal departments.
    parameters: id
    Example Link:
    http://127.0.0.1:8000/datadetails/personal/ireport/?id=300
  
## 9. /moh/requestData (GET API: gets json):
    Function: Ministry of Health requests data from hospital by using this API.
    parameters: ssn and attributes (attributes parameter can be passed multiple times)
    Example Link:
    http://127.0.0.1:8000/moh/requestData/?ssn=30076841161403&attributes=city&attributes=province
  
## 10. /pm/requestMOHForData (GET API: gets json):
    Function: Paramedics requests data from hospital by using this API.
    parameters: ssn and attributes (attributes parameter can be passed multiple times)
    Example Link:
    http://127.0.0.1:8000/pm/requestMOHForData/?ssn=30076841161403&attributes=city&attributes=province&attributes=name&attributes=diagnose
