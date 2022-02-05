from fastapi import APIRouter, Request, Form, File, UploadFile, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from utils import save_file, parsing_csv, parsing_csv_new
from io import StringIO
from db_model.database import SessionLocal, engine # important
from models import Patient, WetSwallow, Rawdata, TimeRecord, MRS, HiatalHernia
import uuid, datetime, crud, pickle
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
        
def init_mrs_metric(length: int):
    temp = {}
    default_metric = {
        "MRS_DCI1": 0,
        "MRS_DCI2": 0,
        "MRS_IRP1": 0,
        "MRS_IRP2": 0
    }
    for index in range(length):
        temp["MRS" + str(index + 1)] = default_metric
    return temp

def init_mrs_drawinfo(length: int):
    temp = {}
    for index in range(length):
        temp["MRS" + str(index + 1)] = []
    return temp 

def init_hh_metric():
    temp = {
        "landmark":{
            "LES-CD": 0,
            "seperate": False
        }
    }
    return temp

def init_hh_drawinfo():
    temp = {"landmark": []}
    return temp

# upload raw data csv 
@router.post("/")
def upload_swallow_file(request:Request, files: UploadFile = File(...), db: Session = Depends(get_db)):
    
    # save csv file 
    df = pd.read_csv(StringIO(str(files.file.read(), 'big5')), encoding='big5', header=None, low_memory=False)
    
    new_df, new_df.columns = df[7:], df.iloc[6]
    save_df, save_df.columns = df[1:], df.iloc[0]

    filename = files.filename
    patient_id = str(df.loc[0,1])[-4:]
    if "ws_10_vigor" in new_df.columns: 
        print(filename, "新資料格式")
        swallow_list, mrs_list, hh_list, catheter_type = parsing_csv_new(new_df)
    else:
        print(filename, "舊資料格式")
        swallow_list, mrs_list, hh_list, catheter_type = parsing_csv(new_df) # swallow_list, mrs_list 都要轉成binary且存入DB
    save_file("./data/basic_test/", filename, save_df) # 儲存助理上傳的csv 

    record_id = uuid.uuid4() # create this patient's UUID
    now_time = datetime.datetime.now() # create current time 

    # INSERT INTO patient_info table;
    db_patient = crud.create_patient(db, Patient.PatientCreate(patient_id=patient_id, record_id=record_id, catheter_type=catheter_type))

    # INSERT INTO Time_Record table;
    db_timerecord = crud.create_timerecord(db, TimeRecord.TimeRecordCreate(record_id=record_id, last_update=now_time, doctor_id=0)) # for Dr.Lei
    db_timerecord = crud.create_timerecord(db, TimeRecord.TimeRecordCreate(record_id=record_id, last_update=now_time, doctor_id=1)) # for Dr.Liang
    db_timerecord = crud.create_timerecord(db, TimeRecord.TimeRecordCreate(record_id=record_id, last_update=now_time, doctor_id=-1))# for MMS

    # INSERT INTO raw_data table
    db_rawdata = crud.create_rawdata(db, Rawdata.RawDataCreate(filename=filename, record_id=record_id, hh_raw=hh_list, ws_10_raw=swallow_list, mrs_raw=mrs_list))

    # INSERT INTO DB with doctor_io = [0, 1, -1]
    for i in [0, 1, -1]:
        db_ws10 = crud.create_ws10(db, WetSwallow.WetSwallowCreate(record_id=record_id, doctor_id=i))
        db_mrs = crud.create_mrs(db, MRS.MrsCreate(record_id=record_id, doctor_id=i, mrs_metric = init_mrs_metric(len(mrs_list)), draw_info = init_mrs_drawinfo(len(mrs_list))))
        db_hh = crud.create_hh(db, HiatalHernia.HiatalHerniaCreate(record_id=record_id, doctor_id=i, hh_metric=init_hh_metric(), draw_info=init_hh_drawinfo()))

    return{
        "status":"success",
    }
