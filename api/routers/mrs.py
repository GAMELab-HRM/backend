from fastapi import APIRouter, Depends
from models import WetSwallow, MRS
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
    prefix="/api/v1/mrs",
    tags=["Multiple rapid swallows"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()

"""
處理MRS raw data 
[GET] 取得mrs的raw data
"""
@router.get("/rawdata")
def get_mrs_rawdata(record_id:UUID, db: Session = Depends(get_db)):
    mrs_rawdata = crud.get_mrs_rawdata(db, record_id)
    retv = pickle.loads(mrs_rawdata[0].mrs_raw)
    retv = json.dumps(retv)
    compressed = zlib.compress(retv.encode())
    ans = {
        "rawdata": compressed
    }
    json_compatible_item_data  = jsonable_encoder(ans, custom_encoder={bytes: lambda v: base64.b64encode(v).decode('utf-8')})
    return json_compatible_item_data

"""
處理MRS EPT-metric
裡面放DCI、IRP等數值
[GET] 前端取得mrs的ept-metrics數值
[PUT] 前端更新mrs的ept-metrics數值
"""
@router.get("/metrics")
def get_mrs_metric(record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    mrs_metric = crud.get_mrs_metric(db, record_id, doctor_id)
    return mrs_metric

@router.put("/metrics", dependencies=[Depends(JWTBearer())])
def update_mrs_metric(request: Dict[Any, Any], record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    mrs_metric = crud.update_mrs_metric(db, request, record_id, doctor_id)
    return mrs_metric

"""
處理MRS 畫線資訊
裡面會放LES、UES在圖上的位置資訊
[GET] 前端取得mrs畫線的資訊
[PUT] 前端更新mrs畫線的資訊
"""
@router.get("/drawinfo")
def get_mrs_drawinfo(record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    mrs_drawinfo = crud.get_mrs_drawinfo(db, record_id, doctor_id)
    return mrs_drawinfo

@router.put("/drawinfo", dependencies=[Depends(JWTBearer())])
def update_mrs_drawinfo(request: Dict[Any, Any], record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    mrs_drawinfo = crud.update_mrs_drawinfo(db, request, record_id, doctor_id)
    return mrs_drawinfo

"""
處理MRS 結果
是否為contractile reserve 
[GET] 前端取得mrs的結果 
[PUT] 前端更新mrs的結果
"""
@router.get("/result", response_model=MRS.MrsResult, dependencies=[Depends(JWTBearer())])
def get_mrs_result(record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    mrs_result = crud.get_mrs_result(db, record_id, doctor_id)
    return MRS.MrsResult(mrs_result = mrs_result)

@router.put("/result", dependencies=[Depends(JWTBearer())])
def update_mrs_result(request: MRS.MrsResult, record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    updated_mrs_result = crud.update_mrs_result(db, request.dict(), record_id, doctor_id)
    return updated_mrs_result

# @router.get("/data/{record_id}", response_model=MRS.MrsGetResponse)
# def get_mrs_data(record_id:UUID, doctor_id:int, db: Session = Depends(get_db)):
#     mrs_data = crud.get_mrs(db, record_id, doctor_id)
#     retv = MRS.MrsGetResponse(
#         draw_info = mrs_data[0].draw_info,
#         mrs_dci = mrs_data[0].mrs_dci,
#         dci_after_mrs = mrs_data[0].dci_after_mrs,
#         irp1 = mrs_data[0].irp1,
#         doctor_id = mrs_data[0].doctor_id,
#         mrs_result = mrs_data[0].mrs_result,
#     )
#     return retv

# @router.put("/data")
# def update_mrs_data(mrs_update_info:MRS.MrsUpdate, db: Session = Depends(get_db)):
#     mrs_update_info = mrs_update_info.dict()
#     retv = crud.update_mrs(db, mrs_update_info)
#     return retv
    
