from fastapi import APIRouter, Request, Form, File ,UploadFile, Depends
from numpy import result_type
from sqlalchemy.orm import Session
from utils import save_file
from models import Table 
from typing import List
from db_model.database import SessionLocal, engine # important
import shutil, crud
from auth.auth_bearer import JWTBearer 

router = APIRouter(
    prefix="/api/v1/table",
    tags=["For frontend's tables"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def check_mrs_draw(mrs_drawinfo: dict) -> bool:
    keys = mrs_drawinfo.keys()
    for k in keys: 
        if len(mrs_drawinfo[k]) == 0:
            return False
    return True 

def check_hh_draw(hh_drawinfo: dict) -> bool: 
    if len(hh_drawinfo['landmark'])==0:
        return False
    return True  

def check_leg_draw(leg_drawinfo: dict) -> bool: 
    if leg_drawinfo == {}:
        return False 
    
    keys = leg_drawinfo.keys()
    for k in keys: 
        if len(leg_drawinfo[k]) == 0:
            return False
    return True 

@router.get("/basic_test/upload", response_model=List[Table.UploadPageTable], dependencies=[Depends(JWTBearer())])
def get_basic_upload_table(db: Session = Depends(get_db)):
    result = crud.get_upload_info(db)
    return result 

@router.get("/basic_test/all")
def get_basic_all_table(db: Session = Depends(get_db)):
    result = crud.get_all_info(db)
    for i in range(len(result)):
        record_id = str(result[i]['record_id'])
        doctor_id = result[i]['doctor_id']
        mrs_drawinfo = crud.get_mrs_drawinfo(db, record_id=record_id, doctor_id=doctor_id)
        hh_drawinfo = crud.get_hh_drawinfo(db, record_id=record_id, doctor_id=doctor_id)
        leg_drawinfo = crud.get_leg_drawinfo(db, record_id=record_id, doctor_id=doctor_id)
        result[i]['mrs_draw'] = check_mrs_draw(mrs_drawinfo)
        result[i]['hh_draw'] = check_hh_draw(hh_drawinfo)
        result[i]['leg_draw'] = check_leg_draw(leg_drawinfo)        
    return result 
    result = [ dict(r) for r in result]
    for i in range(len(result)):
        record_id = str(result[i]['record_id'])
        doctor_id = result[i]['doctor_id']
        mrs_drawinfo = crud.get_mrs_drawinfo(db, record_id=record_id, doctor_id=doctor_id)
        hh_drawinfo = crud.get_hh_drawinfo(db, record_id=record_id, doctor_id=doctor_id)
        result[i]['mrs_draw'] = check_mrs_draw(mrs_drawinfo)
        result[i]['hh_draw'] = check_hh_draw(hh_drawinfo)
        if result[i]['leg_metric'] == {}:
            result[i]['leg_exist'] = False
        else:
            result[i]['leg_exist'] = True
        del result[i]['leg_metric']
    return result

