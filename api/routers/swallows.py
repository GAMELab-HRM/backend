from fastapi import APIRouter, Request, Form, File, UploadFile, Depends
from utils import save_file, preprocess_csv
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
    prefix="/api/v1/swallows",
    tags=["10 wet swallows"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()

@router.get("/rawdata/{record_id}")
def get_ws10_rawdata(record_id:UUID, db: Session = Depends(get_db)):
    ws10_rawdata = crud.get_ws_rawdata(db, record_id)
    retv = pickle.loads(ws10_rawdata[0].ws_10_raw)
    return {
        "rawdata":json.dumps(retv)
    }

@router.get("/data/{record_id}", response_model=WetSwallow.WetSwallowGetResponse)
def get_swallow_data(record_id:UUID, doctor_id:int, db: Session = Depends(get_db)):
    ws_data = crud.get_ws10(db, WetSwallow.WetSwallowGet(record_id=record_id, doctor_id=doctor_id))
    retv = WetSwallow.WetSwallowGetResponse(
        record_id=ws_data[0].record_id,
        vigors=ws_data[0].vigors,
        patterns=ws_data[0].patterns,
        dcis=ws_data[0].dcis,
        swallow_types=ws_data[0].swallow_types,
        irp4s=ws_data[0].irp4s,
        dls=ws_data[0].dls,
        ws_result=ws_data[0].ws_result,
        doctor_id=ws_data[0].doctor_id
    )
    return retv

@router.put("/data")
def update_swallow_data(ws_update_info:WetSwallow.WetSwallowUpdate, db: Session = Depends(get_db)):
    ws_update_info = ws_update_info.dict()
    # 轉換成字典
    print(ws_update_info)
    ws_update_info["vigors"] = ws_update_info["vigors"]
    ws_update_info["patterns"] = ws_update_info["patterns"]
    ws_update_info["dcis"] = ws_update_info["dcis"]
    ws_update_info["swallow_types"] = ws_update_info["swallow_types"]
    ws_update_info["irp4s"] = ws_update_info["irp4s"]
    ws_update_info["dls"] = ws_update_info["dls"]
    retv = crud.update_ws10(db, ws_update_info)
    # crud update swallow 
    return retv
    

