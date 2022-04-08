from fastapi import APIRouter, Depends
from numpy import record
from models import WetSwallow, MRS, HiatalHernia, Leg
from models.Rawdata import WsData 
from sqlalchemy.orm import Session 
from db_model.database import SessionLocal, engine # important
from typing import Dict, Any
import crud, pickle, json, zlib, base64 
import pandas as pd 
from uuid import UUID
from auth.auth_bearer import JWTBearer 
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/api/v1/leg",
    tags=["Leg Wet Swallow"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()

"""
處理Leg Wet Swallow 的 raw data 
[GET] 取得 Leg Wet Swallow 的raw data
"""
@router.get("/rawdata")
def get_leg_rawdata(record_id:UUID, db: Session = Depends(get_db)):
    leg_rawdata = crud.get_leg_rawdata(db, record_id)
    
    #有些資料沒有rawdata
    if leg_rawdata[0][0] == None:
        return {
            "rawdata":json.dumps([])
        }
    else: 
        retv = pickle.loads(leg_rawdata[0].leg_raw)
        retv = json.dumps(retv)
        compressed = zlib.compress(retv.encode())
        ans = {
            "rawdata": compressed
        }
        json_compatible_item_data  = jsonable_encoder(ans, custom_encoder={bytes: lambda v: base64.b64encode(v).decode('utf-8')})
        return json_compatible_item_data

@router.get("/metrics")
def get_leg_metric(record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    leg_metric = crud.get_leg_metric(db, record_id, doctor_id)
    return leg_metric

@router.put("/metrics")
def update_leg_metric(request: Dict[Any, Any], record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    leg_metric = crud.update_leg_metric(db, request, record_id, doctor_id)
    return leg_metric


@router.get("/drawinfo")
def get_leg_drawinfo(record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    leg_drawinfo = crud.get_leg_drawinfo(db, record_id, doctor_id)
    return leg_drawinfo

@router.put("/drawinfo")
def update_leg_drawinfo(request: Dict[Any, Any], record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    leg_drawinfo = crud.update_leg_drawinfo(db, request, record_id, doctor_id)
    return leg_drawinfo


@router.get("/result")
def get_leg_result(record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    leg_result = crud.get_leg_reesult(db, record_id, doctor_id)
    return {
        "SLR_result": leg_result
    }

@router.put("/result")
def update_leg_result(request: Leg.LegResult, record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    request = request.dict()
    temp = {
        "leg_result": request["SLR_result"],
    }
    updated_leg_result = crud.update_leg_result(db, temp, record_id, doctor_id)
    return updated_leg_result