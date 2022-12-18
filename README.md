# FYP-Management-System

PrivacyOps in Smart Cities, FYP code repository.

# How to run:

1. Clone the Repository
2. Go to the folder ./FYP-Management-System
3. Run "pip install -r requirements.txt"

# How to Merge Tables into db:
```
    python CopyTableToAnotherDb.py (Name of db to add table) (Name of db to add table from) (table name)
```

cd "Hospital System/main_system"

# APIs to Call:
## 1. /datadetails/personal/requestForData in hospital_api:

# How to call /requestForData Api:
requesting data:
http://127.0.0.1:8000/datadetails/personal/requestForData/?ssn=4903773748744614&froms=Hospital&tos=Paramedics&attributes=name&attributes=city&attributes=province
http://127.0.0.1:8000/datadetails/personal/requestForData/?ssn=4903773748744614&froms=Hospital&tos=Paramedics&attributes=name&attributes=city
http://127.0.0.1:8000/datadetails/personal/requestForData/?ssn=4903773748744614&froms=Hospital&tos=MinistryOfHealth&attributes=name&attributes=province
http://127.0.0.1:8000/datadetails/personal/requestForData/?ssn=4903773748744614&froms=Hospital&tos=MinistryOfHealth&attributes=city

# How to call /inform API:
I guess just change the requestForData to inform in the above API callings
