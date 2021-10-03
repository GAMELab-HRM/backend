from typing import Optional
from fastapi import FastAPI
from HRMdata import HRMclass
app = FastAPI()

    
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/v1/save")
def save():
    f = open("./data/save.txt","a")
    f.write("now the file hans")
    f.close()
    return "saved"

# return all patient's HRM data     
@app.get("/api/v1/user/data")
def get_user_data():
    # /code/data/all_patient.csv (will mount in container )
    return "testing NGINX reverse proxy"

# add new user's hrm data 
@app.post("/api/v1/user/data")
def add_data(data:HRMclass):
    return data

@app.put("/api/v1/user/data")
def put_data(data:HRMclass):
    return data 



