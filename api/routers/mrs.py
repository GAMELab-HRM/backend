from fastapi import APIRouter, Request, Form, File, UploadFile, Depends
from utils import save_file, process_10swallow, preprocess_csv
from models.WetSwallow import WetSwallowCreate
from models import WetSwallow
from models.Rawdata import WsData 
from sqlalchemy.orm import Session 
from db_model.database import SessionLocal, engine # important
from io import StringIO
import shutil, copy, crud, pickle, json
import pandas as pd 
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

router = APIRouter(
    prefix="/api/v1/mrs",
    tags=["Multiple rapid swallows"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()

@router.get("/rawdata/{record_id}")
def get_mrs_rawdata(record_id:UUID, db: Session = Depends(get_db)):
    mrs_rawdata = crud.get_mrs_rawdata(db, record_id)
    retv = pickle.loads(mrs_rawdata[0].mrs_raw)
    print(len(retv))
    return {
        "rawdata":json.dumps(retv)
    }
@router.get("/data")
def get_mrs_data():
    return{"msg":"Hello hiatal datas"}

@router.post("/data")
def add_mrs_data():
    return{"msg":"add mrs data"}
    
@router.put("/data")
def update_mrs_data():
    return {"msg":"update mrs data"}

