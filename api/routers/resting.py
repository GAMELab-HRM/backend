from fastapi import APIRouter, Depends
from numpy import record
from models import WetSwallow, MRS, HiatalHernia, Resting
from sqlalchemy.orm import Session 
from db_model.database import SessionLocal, engine # important
from typing import Dict, Any
import crud, pickle, json, zlib, base64 
import pandas as pd 
from uuid import UUID
from auth.auth_bearer import JWTBearer 
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/api/v1/resting",
    tags=["Resting"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()

"""
處理Resting 的 raw data 
[GET] 取得Resting的raw data
"""
@router.get("/rawdata")
def get_resting_rawdata(record_id:UUID, db: Session = Depends(get_db)):
    resting_rawdata = crud.get_resting_rawdata(db, record_id)
    retv = pickle.loads(resting_rawdata[0].resting_raw)
    retv = json.dumps(retv)
    compressed = zlib.compress(retv.encode())
    ans = {
        "rawdata": compressed
    }
    json_compatible_item_data  = jsonable_encoder(ans, custom_encoder={bytes: lambda v: base64.b64encode(v).decode('utf-8')})
    return json_compatible_item_data

"""
處理resting 的 EPT-metric
裡面放LES-CD等數值
[GET] 前端取得resting的metrics數值
[PUT] 前端更新resting的metrics數值
"""
@router.get("/metrics")
def get_resting_metric(record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    resting_metric = crud.get_resting_metric(db, record_id, doctor_id)
    return resting_metric

@router.put("/metrics", dependencies=[Depends(JWTBearer())])
def update_resting_metric(request: Dict[Any, Any], record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    resting_metric = crud.update_resting_metric(db, request, record_id, doctor_id)
    return resting_metric

"""
處理resting 畫線資訊
裡面會放LES、UES等在圖上的位置資訊
[GET] 前端取得resting畫線的資訊
[PUT] 前端更新resting畫線的資訊
"""
@router.get("/drawinfo")
def get_resting_drawinfo(record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    resting_drawinfo = crud.get_resting_drawinfo(db, record_id, doctor_id)
    return resting_drawinfo

@router.put("/drawinfo", dependencies=[Depends(JWTBearer())])
def update_resting_drawinfo(request: Dict[Any, Any], record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    resting_drawinfo = crud.update_resting_drawinfo(db, request, record_id, doctor_id)
    return resting_drawinfo

"""
處理resting result資訊
裡面會放hh_result、rip_result等在圖上的位置資訊
[GET] 前端取得hiatal hernia result 的資訊
[PUT] 前端更新hiatal hernia result 的資訊
"""
@router.get("/result", response_model = Resting.RestingResult)
def get_resting_result(record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    hh_result, rip_result = crud.get_resting_result(db, record_id, doctor_id)
    print(hh_result, rip_result)
    return Resting.RestingResult(resting_result = hh_result, rip_result = rip_result)

@router.put("/result", dependencies=[Depends(JWTBearer())])
def update_resting_result(request: Resting.RestingResult, record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    request = request.dict()
    temp = {
        "resting_result": request["resting_result"],
        "rip_result": request["rip_result"]
    }
    updated_resting_result = crud.update_resting_result(db, temp, record_id, doctor_id)
    return updated_resting_result