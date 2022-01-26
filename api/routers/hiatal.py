from fastapi import APIRouter, Depends
from numpy import record
from models import WetSwallow, MRS, HiatalHernia
from models.Rawdata import WsData 
from sqlalchemy.orm import Session 
from db_model.database import SessionLocal, engine # important
from typing import Dict, Any
import crud, pickle, json
import pandas as pd 
from uuid import UUID
from auth.auth_bearer import JWTBearer 
router = APIRouter(
    prefix="/api/v1/hh",
    tags=["Hiatal hernia"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()

"""
處理hiatal hernia 的 raw data 
[GET] 取得hiatal hernia的raw data
"""
@router.get("/rawdata", dependencies=[Depends(JWTBearer())])
def get_hh_rawdata(record_id:UUID, db: Session = Depends(get_db)):
    hh_rawdata = crud.get_hh_rawdata(db, record_id)
    retv = pickle.loads(hh_rawdata[0].hh_raw)
    return {
        "rawdata":json.dumps(retv)
    }

"""
處理hiatal hernia 的 EPT-metric
裡面放LES-CD等數值
[GET] 前端取得hiatal hernia的metrics數值
[PUT] 前端更新hiatal hernia的metrics數值
"""
@router.get("/metrics", dependencies=[Depends(JWTBearer())])
def get_hh_metric(record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    mrs_metric = crud.get_hh_metric(db, record_id, doctor_id)
    return mrs_metric

@router.put("/metrics", dependencies=[Depends(JWTBearer())])
def update_hh_metric(request: Dict[Any, Any], record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    mrs_metric = crud.update_hh_metric(db, request, record_id, doctor_id)
    return mrs_metric

"""
處理hiatal hernia 畫線資訊
裡面會放LES、UES等在圖上的位置資訊
[GET] 前端取得hiatal hernia畫線的資訊
[PUT] 前端更新hiatal hernia畫線的資訊
"""
@router.get("/drawinfo", dependencies=[Depends(JWTBearer())])
def get_hh_drawinfo(record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    hh_drawinfo = crud.get_hh_drawinfo(db, record_id, doctor_id)
    return hh_drawinfo

@router.put("/drawinfo", dependencies=[Depends(JWTBearer())])
def update_hh_drawinfo(request: Dict[Any, Any], record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    mrs_drawinfo = crud.update_hh_drawinfo(db, request, record_id, doctor_id)
    return mrs_drawinfo

"""
處理hiatal hernia result資訊
裡面會放hh_result、rip_result等在圖上的位置資訊
[GET] 前端取得hiatal hernia result 的資訊
[PUT] 前端更新hiatal hernia result 的資訊
"""
@router.get("/result", response_model = HiatalHernia.HiatalHerniaResult, dependencies=[Depends(JWTBearer())])
def get_hh_result(record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    hh_result, rip_result = crud.get_hh_reesult(db, record_id, doctor_id)
    print(hh_result, rip_result)
    return HiatalHernia.HiatalHerniaResult(hh_result = hh_result, rip_result = rip_result)

@router.put("/result", dependencies=[Depends(JWTBearer())])
def update_hh_result(request: HiatalHernia.HiatalHerniaResult, record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    request = request.dict()
    temp = {
        "hiatal_hernia_result": request["hh_result"],
        "rip_result": request["rip_result"]
    }
    updated_hh_result = crud.update_hh_result(db, temp, record_id, doctor_id)
    return updated_hh_result