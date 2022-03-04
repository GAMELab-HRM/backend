from fastapi import APIRouter, Request, Form, File, UploadFile, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from utils import save_file, parsing_csv, parsing_csv_new
from io import StringIO
from db_model.database import SessionLocal, engine # important
from models import Patient, WetSwallow, Rawdata, TimeRecord, MRS, HiatalHernia, Leg
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

def init_leg_metric(length: int):
    temp = {}
    default_metric = {
        "LEG_DCI1": 0,
        "LEG_DCI2": 0,
        "LEG_IRP1": 0,
        "LEG_IRP2": 0
    }
    for index in range(length):
        temp["LEG" + str(index + 1)] = default_metric
    return temp

def init_leg_drawinfo(length: int):
    temp = {}
    for index in range(length):
        temp["LEG" + str(index + 1)] = []
    return temp 

@router.post("/leg")
def upload_swallow_file(record_id: UUID, request:Request, files: UploadFile = File(...),  db: Session = Depends(get_db)):
    
    # save csv file 
    df = pd.read_csv(StringIO(str(files.file.read(), 'big5')), encoding='big5', header=None, low_memory=False)
    
    new_df, new_df.columns = df[7:], df.iloc[6]
    save_df, save_df.columns = df[1:], df.iloc[0]

    filename = files.filename
    patient_id = str(df.loc[0,1])[-4:]
    if "ws_10_vigor" in new_df.columns: 
        print(filename, "新資料格式")
        swallow_list, swallow_index, mrs_list, mrs_index, hh_list, hh_index, leg_list, leg_index, catheter_type, all_data = parsing_csv_new(new_df)
    else:
        print(filename, "舊資料格式")
        swallow_list, swallow_index, mrs_list, mrs_index, hh_list, hh_index, leg_list, leg_index, catheter_type, all_data = parsing_csv(new_df) # swallow_list, mrs_list 都要轉成binary且存入DB
    
    """
    更新rawdata table
    """
    updated_leg = db.query(dbmodels.Raw_Data).filter(
        (dbmodels.Raw_Data.record_id==record_id)
    ).update({"leg_raw":pickle.dumps(leg_list), "leg_index":leg_index})
    db.commit()
    db.flush()
    
    """
    更新Leg table 
    (先前上傳的資料 在這個table上是沒有任何資料的)
    所以手動補上那些值
    """
    for i in [0, 1, -1]:
        db_leg = crud.create_leg(db, Leg.LegCreate(record_id=record_id, doctor_id=i, leg_metric = init_leg_metric(len(leg_list)), draw_info = init_leg_drawinfo(len(leg_list))))
    return updated_leg


