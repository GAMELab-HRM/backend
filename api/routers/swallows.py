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
from auth.auth_bearer import JWTBearer 

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

# 取得特定病人的hrm rawdata
@router.get("/rawdata/{record_id}", dependencies=[Depends(JWTBearer())])
def get_ws10_rawdata(record_id:UUID, db: Session = Depends(get_db)):
    ws10_rawdata = crud.get_ws_rawdata(db, record_id)
    retv = pickle.loads(ws10_rawdata[0].ws_10_raw)
    return {
        "rawdata":json.dumps(retv)
    }

# 取得特定病人的data
@router.get("/data", response_model=WetSwallow.WetSwallowGetResponse, dependencies=[Depends(JWTBearer())])
def get_swallow_data(record_id:UUID, doctor_id:int, db: Session = Depends(get_db)):
    ws_data = crud.get_ws10(db, WetSwallow.WetSwallowGet(record_id=record_id, doctor_id=doctor_id))
    retv = WetSwallow.WetSwallowGetResponse(
        record_id=ws_data[0].record_id,
        vigors=ws_data[0].vigors,
        patterns=ws_data[0].patterns,
        dcis=ws_data[0].dcis,
        breaks=ws_data[0].breaks,
        swallow_types=ws_data[0].swallow_types,
        irp4s=ws_data[0].irp4s,
        dls=ws_data[0].dls,
        ws_result=ws_data[0].ws_result,
        doctor_id=ws_data[0].doctor_id
    )
    return retv

# 更新特定病人的data
@router.put("/data", dependencies=[Depends(JWTBearer())])
def update_swallow_data(ws_update_info:WetSwallow.WetSwallowUpdate, db: Session = Depends(get_db)):
    ws_update_info = ws_update_info.dict()
    retv = crud.update_ws10(db, ws_update_info)
    return retv
    

