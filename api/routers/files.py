from fastapi import APIRouter, Request, Form, File, UploadFile, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from utils import save_file, preprocess_csv, parsing_csv
from io import StringIO
from db_model.database import SessionLocal, engine # important
from models import Patient, WetSwallow, Rawdata, TimeRecord, MRS, HiatalHernia
import shutil, copy, uuid, datetime, crud, pickle
import pandas as pd 

router = APIRouter(
    prefix="/api/v1/files",
    tags=["for csv files"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# upload raw data csv 
@router.post("/")
def upload_swallow_file(request:Request, files: UploadFile = File(...), db: Session = Depends(get_db)):
    
    # save csv file 
    df = pd.read_csv(StringIO(str(files.file.read(), 'big5')), encoding='big5', header=None)
    new_df, new_df.columns = df[7:], df.iloc[6]
    save_df, save_df.columns = df[1:], df.iloc[0]

    filename = files.filename
    patient_id = str(df.loc[0,1])[-4:]
    swallow_list, mrs_list, sensor_num = parsing_csv(new_df) # swallow_list, mrs_list 都要轉成binary且存入DB
    save_file("./data/basic_test/", filename, save_df) # 儲存助理上傳的csv 

    record_id = uuid.uuid4() # create this patient's UUID
    now_time = datetime.datetime.now() # create current time 

    # INSERT INTO patient_info table;
    db_patient = crud.create_patient(db, Patient.PatientCreate(patient_id=patient_id, record_id=record_id, sensor_num=sensor_num))

    # INSERT INTO Time_Record table;
    db_timerecord = crud.create_timerecord(db, TimeRecord.TimeRecordCreate(record_id=record_id, last_update=now_time, doctor_id=0)) # for Dr.Lei
    db_timerecord = crud.create_timerecord(db, TimeRecord.TimeRecordCreate(record_id=record_id, last_update=now_time, doctor_id=1)) # for Dr.Liang
    db_timerecord = crud.create_timerecord(db, TimeRecord.TimeRecordCreate(record_id=record_id, last_update=now_time, doctor_id=-1))# for MMS

    # INSERT INTO raw_data table
    db_rawdata = crud.create_rawdata(db, Rawdata.RawDataCreate(filename=filename, record_id=record_id, ws_10_raw=swallow_list, mrs_raw=mrs_list))

    # INSERT INTO DB with doctor_io = [0, 1, -1]
    for i in [0, 1, -1]:
        db_ws10 = crud.create_ws10(db, WetSwallow.WetSwallowCreate(record_id=record_id, doctor_id=i))
        db_mrs = crud.create_mrs(db, MRS.MrsCreate(record_id=record_id, doctor_id=i))
        db_hh = crud.create_hh(db, HiatalHernia.HiatalHerniaCreate(record_id=record_id, doctor_id=i))

    return{
        "status":"success",
    }
