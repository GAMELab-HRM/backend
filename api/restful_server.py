from typing import Optional
from fastapi import FastAPI, Request, Form, File ,UploadFile
from models.HRMdata import HRMclass
from models.HRMdata import CustomClass
from routers import hiatal, swallows, mrs, rdc
from utils import *
import shutil

# create app instance 
app = FastAPI()

# FastAPI router 
app.include_router(hiatal.router)
app.include_router(swallows.router)
app.include_router(mrs.router)
app.include_router(rdc.router)
    
@app.get("/")
def read_root():
    return {"Hello": "World"}

# add new user's hrm data 
@app.post("/api/v1/swallow/data")
def add_data(data:CustomClass):
    process_10swallow(data.GT)
    process_10swallow(data.MMS)
    return data

@app.put("/api/v1/swallow/data")
def put_data(data:HRMclass):
    return data 



