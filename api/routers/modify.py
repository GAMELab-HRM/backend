from re import L
from fastapi import APIRouter, Request, Form, File, UploadFile, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from utils import save_file, parsing_csv, parsing_csv_new
from io import StringIO
from db_model.database import SessionLocal, engine # important
from models import Patient, WetSwallow, Rawdata, TimeRecord, MRS, HiatalHernia, Leg, Air, Resting
import uuid, datetime, crud, pickle, json
import pandas as pd 
import db_model.models as dbmodels 
from uuid import UUID

router = APIRouter(
    prefix="/api/v1/modify",
    tags=["人工改寫database"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()
def init_air_metric(length: int):
    temp = {}
    if length!=0:
        temp["dcis"] = [0 for i in range(length)]
        temp["irp4s"] = [0 for i in range(length)]
        temp["dls"] = [0 for i in range(length)]
        temp["breaks"] = [0 for i in range(length)]
        temp["SPR"] = 0
        temp["ERL"] = 0
    return temp
def init_leg_metric(length: int):
    temp = {}
    default_metric = {
        "abdominal_SLR_max": 0,
        "abdominal_SLR_mean": 0,
        "abdominal_baseline_max": 0,
        "abdominal_baseline_mean": 0,
        "esophageal_SLR_max": 0,
        "esophageal_SLR_mean": 0,
        "esophageal_baseline_max": 0,
        "esophageal_baseline_mean": 0,       
        "esophageal_pressure_ratio_max": 0,
        "esophageal_pressure_ratio_mean": 0
    }
    for index in range(length):
        temp["SLR" + str(index + 1)] = default_metric
    return temp

def init_leg_drawinfo(length: int):
    temp = {}
    for index in range(length):
        temp["SLR" + str(index + 1)] = []
    return temp 

def init_resting_metric(length: int):
    temp = {}
    default_resting = {
        "LES-CD": 0,
        "seperate": False
    }
    for index in range(length): 
        temp["Resting" + str(index + 1)] = default_resting
    return temp

def init_resting_drawinfo(length: int):
    temp = {}
    for index in range(length):
        temp["Resting" + str(index + 1)] = []
    return temp

def init_resting_result(length: int):
    return ["None" for i in range(length)]

@router.post("/resting")
def upload_resting_file(record_id: UUID, request:Request, files: UploadFile = File(...),  db: Session = Depends(get_db)):
    df = pd.read_csv(StringIO(str(files.file.read(), 'big5')), encoding='big5', header=None, low_memory=False)
    new_df, new_df.columns = df[7:], df.iloc[6]
    save_df, save_df.columns = df[1:], df.iloc[0]
    filename = files.filename
    patient_id = str(df.loc[0,1])[-4:]
    if "ws_10_vigor" in new_df.columns: 
        print(filename, "新資料格式")
        swallow_list, swallow_index, mrs_list, mrs_index, hh_list, hh_index, leg_list, leg_index, air_index, resting_list, resting_index, catheter_type, all_data = parsing_csv_new(new_df)
    else:
        print(filename, "舊資料格式")
        swallow_list, swallow_index, mrs_list, mrs_index, hh_list, hh_index, leg_list, leg_index, air_index, resting_list, resting_index, catheter_type, all_data = parsing_csv(new_df) # swallow_list, mrs_list 都要轉成binary且存入DB
    
    """
    更新rawdata table
    """
    updated_resting = db.query(dbmodels.Raw_Data).filter(
        (dbmodels.Raw_Data.record_id==record_id)
    ).update({"resting_raw":pickle.dumps(resting_list), "resting_index":resting_index})
    db.commit()
    db.flush()
    
    """
    更新Resting table 
    (先前上傳的資料 在這個table上是沒有任何資料的)
    所以手動補上那些值
    """
    resting_modify = False
    resting_patient = db.query(dbmodels.Resting.record_id).filter(dbmodels.Resting.record_id==record_id).all()
    if len(resting_patient)==0:
        for i in [0, 1, -1]:
            db_resting = crud.create_resting(db, Resting.RestingCreate(record_id=record_id, doctor_id=i, resting_result = init_resting_result(len(resting_list)), rip_result = init_resting_result(len(resting_list)),resting_metric=init_resting_metric(len(resting_list)), draw_info=init_resting_drawinfo(len(resting_list))))
        resting_modify = True 
    
    return  {
        "resting":resting_modify,
    }
# HRM 0303
@router.post("/leg")
def upload_swallow_file(record_id: UUID, request:Request, files: UploadFile = File(...),  db: Session = Depends(get_db)):
    df = pd.read_csv(StringIO(str(files.file.read(), 'big5')), encoding='big5', header=None, low_memory=False)
    new_df, new_df.columns = df[7:], df.iloc[6]
    save_df, save_df.columns = df[1:], df.iloc[0]
    filename = files.filename
    patient_id = str(df.loc[0,1])[-4:]
    if "ws_10_vigor" in new_df.columns: 
        print(filename, "新資料格式")
        swallow_list, swallow_index, mrs_list, mrs_index, hh_list, hh_index, leg_list, leg_index, air_index, catheter_type, all_data = parsing_csv_new(new_df)
    else:
        print(filename, "舊資料格式")
        swallow_list, swallow_index, mrs_list, mrs_index, hh_list, hh_index, leg_list, leg_index, air_index, catheter_type, all_data = parsing_csv(new_df) # swallow_list, mrs_list 都要轉成binary且存入DB
    
    """
    更新rawdata table
    """
    updated_leg = db.query(dbmodels.Raw_Data).filter(
        (dbmodels.Raw_Data.record_id==record_id)
    ).update({"leg_raw":pickle.dumps(leg_list), "leg_index":leg_index})
    db.commit()
    db.flush()
    
    leg_modify = False 
    air_modify = False 
    """
    更新Air table
    """
    air_patient = db.query(dbmodels.Air.record_id).filter(dbmodels.Air.record_id==record_id).all()
    if len(air_patient)==0:
        for i in [0, 1, -1]:
            db_air = crud.create_air(db, Air.AirCreate(record_id=record_id, doctor_id=i, air_metric = init_air_metric(len(air_index))))
        air_modify = True 
    """
    更新Leg table 
    (先前上傳的資料 在這個table上是沒有任何資料的)
    所以手動補上那些值
    """
    leg_patient = db.query(dbmodels.Leg.record_id).filter(dbmodels.Leg.record_id==record_id).all()
    if len(leg_patient)==0:
        for i in [0, 1, -1]:
            db_leg = crud.create_leg(db, Leg.LegCreate(record_id=record_id, doctor_id=i, leg_metric = init_leg_metric(len(leg_list)), draw_info = init_leg_drawinfo(len(leg_list))))
        leg_modify = True 
    
    return  {
        "leg":leg_modify,
        "air":air_modify
    }

