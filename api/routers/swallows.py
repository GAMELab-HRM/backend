from fastapi import APIRouter 
from fastapi import Request, Form, File ,UploadFile
from utils import save_file, process_10swallow, preprocess_csv
from models.WetSwallow import WetSwallowCreate
from models.Rawdata import WsData 
from io import StringIO
import crud
import shutil, copy
import pandas as pd 


router = APIRouter(
    prefix="/api/v1/swallows",
    tags=["10 wet swallows"]
)


@router.get("/data")
def get_swallow_data():
    return{"msg":"Hello swallow datas"}

@router.post("/data")
def add_swallow_data(data):
    process_10swallow(data.GT)
    process_10swallow(data.MMS)
    return {"msg":"add new swallow data"}

@router.put("/data")
def update_swallow_data():
    return {"msg":"updated"}
    

@router.post("/")
def create_swallow(data:WetSwallowCreate):
    crud.create_ws10(data)
    return {"msg":"create swallow data "}
