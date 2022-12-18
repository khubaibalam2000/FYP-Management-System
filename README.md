# FYP-Management-System

PrivacyOps in Smart Cities, FYP code repository.

# How to run:

1. Clone the Repository
2. Go to the folder ./FYP-Management-System
3. Run "pip install -r requirements.txt"
4. Go the ./FYP-Management-System/Hospital System/main_system, and then run 'python manage.py runserver'.

# How to Merge Tables into db:
```
    python CopyTableToAnotherDb.py (Name of db to add table) (Name of db to add table from) (table name)
```

cd "Hospital System/main_system"

# APIs to Call:
## 1. /datadetails/personal/requestForData in hospital_api (GET API: gets json):
    parameters: ssn, froms, tos, attributes (attributes parameter can be passed multiple times)
    Example Link:
    http://127.0.0.1:8000/datadetails/personal/requestForData/?ssn=4903773748744614&froms=Hospital&tos=Paramedics&attributes=name&attributes=city&attributes=province
    http://127.0.0.1:8000/datadetails/personal/requestForData/?ssn=4903773748744614&froms=Hospital&tos=MinistryOfHealth&attributes=name&attributes=province
    
## 2. /datadetails/personal/inform in hospital_api (GET API: gets json):
    parameters: ssn, froms, tos, attributes (attributes parameter can be passed multiple times)
    Example Link:
    http://127.0.0.1:8000/datadetails/personal/requestForData/?ssn=4903773748744614&froms=Hospital&tos=Paramedics&attributes=name&attributes=city&attributes=province
    http://127.0.0.1:8000/datadetails/personal/requestForData/?ssn=4903773748744614&froms=Hospital&tos=MinistryOfHealth&attributes=name&attributes=province
    
## 3. /datadetails/personal/epdgwithconnection (GET API: gets image png):
    parameters: ssn
    http://127.0.0.1:8000/datadetails/personal/epdgwithconnection/?ssn=4903773748744614
    
## 4. /datadetails/personal/epdgwithoutconnection (GET API: gets .html file):
    parameters: ssn
    Example Link:
    http://127.0.0.1:8000/datadetails/personal/epdgwithoutconnection/?ssn=4903773748744614
    
## 5. /datadetails/personal/ipdg (GET API: gets .html file):
    parameters: id
    Example Link:
    http://127.0.0.1:8000/datadetails/personal/ipdg/?id=400
    
## 6. /datadetails/personal/eXdataReport (GET API: gets .pdf file):
    parameters: ssn
    Example Link:
    http://127.0.0.1:8000/datadetails/personal/eXdataReport/?ssn=4903773748744614
    
## 7. /datadetails/personal/eHdataReport (GET API: gets .pdf file):
    parameters: ssn
    Example Link:
    http://127.0.0.1:8000/datadetails/personal/eHdataReport/?ssn=4903773748744614
    
## 8. /datadetails/personal/ireport (GET API: gets .pdf file):
    parameters: id
    Example Link:
    http://127.0.0.1:8000/datadetails/personal/ireport/?id=300
  
## 9. /moh/requestData (GET API: gets json):
    parameters: ssn and attributes (attributes parameter can be passed multiple times)
    Example Link:
    http://127.0.0.1:8000/moh/requestData/?ssn=30076841161403&attributes=city&attributes=province
  
## 10. /pm/requestMOHForData (GET API: gets json):
    parameters: ssn and attributes (attributes parameter can be passed multiple times)
    Example Link:
    http://127.0.0.1:8000/pm/requestMOHForData/?ssn=30076841161403&attributes=city&attributes=province&attributes=name&attributes=diagnose
