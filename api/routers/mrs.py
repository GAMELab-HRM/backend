from fastapi import APIRouter, Request, Form, File, UploadFile, Depends
from utils import save_file, process_10swallow, preprocess_csv
from models.WetSwallow import WetSwallowCreate
from models import WetSwallow, MRS
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

@router.get("/data/{record_id}", response_model=MRS.MrsGetResponse)
def get_mrs_data(record_id:UUID, doctor_id:int, db: Session = Depends(get_db)):
    mrs_data = crud.get_mrs(db, record_id, doctor_id)
    # mrs_data[0]
    retv = MRS.MrsGetResponse(
        mrs_dci_position = mrs_data[0].mrs_dci_position,
        mrs_dci = mrs_data[0].mrs_dci,
        dci_after_mrs_position = mrs_data[0].dci_after_mrs_position,
        dci_after_mrs = mrs_data[0].dci_after_mrs,
        irp1_position = mrs_data[0].irp1_position,
        irp1 = mrs_data[0].irp1,
        doctor_id = mrs_data[0].doctor_id,
        mrs_result = mrs_data[0].mrs_result,
    )
    return retv

@router.put("/data")
def update_mrs_data(ws_update_info:WetSwallow.WetSwallowUpdate, db: Session = Depends(get_db)):
    # ws_update_info = ws_update_info.dict()
    
    # print(ws_update_info)
    # ws_update_info["vigors"] = ws_update_info["vigors"]
    # ws_update_info["patterns"] = ws_update_info["patterns"]
    # ws_update_info["dcis"] = ws_update_info["dcis"]
    # ws_update_info["swallow_types"] = ws_update_info["swallow_types"]
    # ws_update_info["irp4s"] = ws_update_info["irp4s"]
    # ws_update_info["dls"] = ws_update_info["dls"]
    # retv = crud.update_ws10(db, ws_update_info)
   
    return 0
    
