from typing import Optional
from fastapi import FastAPI, Request, Form, File ,UploadFile
from fastapi.middleware.cors import CORSMiddleware
from models.HRMdata import HRMclass
from models.HRMdata import CustomClass
from models.Person import Persontest
from models.Rawdata import RawDataclass
from models.Rawdata import WsData 
from io import StringIO
from routers import hiatal, swallows, mrs, rdc
from utils import *
import shutil
import pandas as pd 

# create app instance 
app = FastAPI()

# CORS 
"""
JUST FOR DEVELOPING
"""
origins = ["http://140.118.157.26:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FastAPI router 
app.include_router(hiatal.router)
app.include_router(swallows.router)
app.include_router(mrs.router)
app.include_router(rdc.router)
    
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/test")
def testing(data:Persontest):
    print(data)
    return {"msg":"testing is ok "}
    
@app.get("/demo", response_model = WsData)
def demo():
    df = pd.read_csv("./1375-normal.CSV")
    filename = "1375-normal.CSV"
    raw_data_string, swallow_index, sensor_num = preprocess_csv(df)
    return{
        "filename": filename,
        "raw": raw_data_string,
        "index": swallow_index,
        "sensors": sensor_num
    }
@app.get("/demo2", response_model = WsData)
def demo2():
    df = pd.read_csv("./2349-normal.CSV")
    filename = "2349-normal.CSV"
    raw_data_string, swallow_index, sensor_num = preprocess_csv(df)
    return{
        "filename": filename,
        "raw": raw_data_string,
        "index": swallow_index,
        "sensors": sensor_num
    }

@app.post("/file", response_model=RawDataclass)
def test_post(request:Request, files: UploadFile = File(...)):
    df = pd.read_csv(StringIO(str(files.file.read(), 'big5')), encoding='big5', skiprows=6)

    print(df.head())

    ans = preprocess_csv(df)
    return ans
    # return {
    #     "status":"demoing",
    #     "file size": 0,
    #     "file name": files.filename
    # }