
from fastapi import APIRouter, Request, Form, File, UploadFile, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from utils import save_file, parsing_csv, parsing_csv_new
from io import StringIO
from db_model.database import SessionLocal, engine # important
from models import Patient, WetSwallow, Rawdata, TimeRecord, MRS, HiatalHernia, Leg, Air, Resting
import uuid, datetime, crud, pickle, json
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
# upload raw data csv 
@router.post("/")
def upload_swallow_file(request:Request, files: UploadFile = File(...), db: Session = Depends(get_db)):
    
    # save csv file 
    df = pd.read_csv(StringIO(str(files.file.read(), 'big5')), encoding='big5', header=None, low_memory=False)
    
    new_df, new_df.columns = df[7:], df.iloc[6]
    save_df, save_df.columns = df[1:], df.iloc[0]

    filename = files.filename
    #patient_id = str(df.loc[0,1])[-4:]
    patient_id = filename.split("-")[0]
    if "ws_10_vigor" in new_df.columns: 
        print(filename, "新資料格式")
        swallow_list, swallow_index, mrs_list, mrs_index, hh_list, hh_index, leg_list, leg_index, air_index, resting_list, resting_index, catheter_type, all_data = parsing_csv_new(new_df)
    else:
        print(filename, "舊資料格式")
        swallow_list, swallow_index, mrs_list, mrs_index, hh_list, hh_index, leg_list, leg_index, air_index, resting_list, resting_index, catheter_type, all_data = parsing_csv(new_df) # swallow_list, mrs_list 都要轉成binary且存入DB
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
    # print("WS 10 index", swallow_index)
    # print("MRS index", mrs_index)
    # print("HH index", hh_index)
    db_rawdata = crud.create_rawdata(db, Rawdata.RawDataCreate(
        filename=filename, record_id=record_id, hh_raw=hh_list, ws_10_raw=swallow_list, mrs_raw=mrs_list, leg_raw=leg_list, resting_raw = resting_list,
        ws_10_index = swallow_index, mrs_index=mrs_index, hh_index=hh_index, leg_index=leg_index, all_raw=all_data, resting_index = resting_index,
    ))

    # INSERT INTO DB with doctor_io = [0, 1, -1]
    for i in [0, 1, -1]:
        db_ws10 = crud.create_ws10(db, WetSwallow.WetSwallowCreate(record_id=record_id, doctor_id=i))
        db_mrs = crud.create_mrs(db, MRS.MrsCreate(record_id=record_id, doctor_id=i, mrs_metric = init_mrs_metric(len(mrs_list)), draw_info = init_mrs_drawinfo(len(mrs_list))))
        db_hh = crud.create_hh(db, HiatalHernia.HiatalHerniaCreate(record_id=record_id, doctor_id=i, hh_metric=init_hh_metric(), draw_info=init_hh_drawinfo()))
        db_leg = crud.create_leg(db, Leg.LegCreate(record_id=record_id, doctor_id=i, leg_metric=init_leg_metric(len(leg_list)), draw_info=init_leg_drawinfo(len(leg_list))))
        db_air = crud.create_air(db, Air.AirCreate(record_id=record_id, doctor_id=i, air_metric=init_air_metric(len(air_index))))
        db_resting = crud.create_resting(db, Resting.RestingCreate(record_id=record_id, doctor_id=i, resting_result = init_resting_result(len(resting_list)), rip_result = init_resting_result(len(resting_list)),resting_metric=init_resting_metric(len(resting_list)), draw_info=init_resting_drawinfo(len(resting_list))))
    print("resting index", resting_index)
    return{
        "status":"success",
    }
