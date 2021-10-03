from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()
class HRMdata(BaseModel):
    id: str # 身份證字號
    vigor: list # contraction vigor
    pattern: list # contraction pattern 
    swallow_type: str # swallow type 
    irp: float # IRP4
    dci: float # DCI
    
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
    return "testing NGINX reverse proxy"

@app.post("/api/v1/user/data")
def add_data(data:HRMdata):
    return data






