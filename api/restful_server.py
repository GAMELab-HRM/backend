from typing import Optional
from fastapi import FastAPI, Request, Form, File ,UploadFile
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db 
from fastapi.middleware.cors import CORSMiddleware
from models.Rawdata import RawDataclass
from models.Rawdata import WsData 
from io import StringIO
from routers import hiatal, swallows, mrs, rdc, patient, files, table
from utils import *
import shutil
import pandas as pd 
from typing import List 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# create app instance 
app = FastAPI()

# CORS 
"""
JUST FOR DEVELOPING
"""
origins = ["http://140.118.157.26:8080",]
#origins = ["*",]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#app.add_middleware(DBSessionMiddleware, db_url="postgresql://postgres:password@127.0.0.1:5432/postgres")

engine = create_engine("postgresql://postgres:password@127.0.0.1:5432/postgres")
print(engine.table_names())
# FastAPI router 
app.include_router(hiatal.router)
app.include_router(swallows.router)
app.include_router(mrs.router)
app.include_router(rdc.router)
app.include_router(patient.router)
app.include_router(files.router)
app.include_router(table.router)

    
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def post_root():
    return {"Hello": "World"}
    
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

@app.post("/file")
def test_multiple_file_upload(request:Request, files: List[UploadFile] = File(...)):

    """
    TODO:
        check raw.csv already in Database ?
    """
    for f in files:
        df = pd.read_csv(StringIO(str(f.file.read(), 'big5')), encoding='big5', skiprows=6)
        filename = f.filename 
        print(filename)
        raw_data_string, swallow_index, sensor_num = preprocess_csv(df)
        save_file("./data/wet_swallows/", filename, df)


    return{
        "msg":"ok"
    }