from fastapi import APIRouter, Request, Form, File, UploadFile, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from utils import save_file, process_10swallow, preprocess_csv
from models.Rawdata import WsData 
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

    """
    TODO:
        check raw.csv already in Database ?
    """
    # save csv file 
    # df = pd.read_csv(StringIO(str(files.file.read(), 'big5')), encoding='big5', skiprows=6)
    # filename = files.filename
    # raw_data_string, swallow_index, sensor_num = preprocess_csv(df)
    # save_file("./data/", filename, df)

    record_id = uuid.uuid4()
    patient_id = "A122973323"
    sensor_num = 20
    filename = "3323-normal.csv"
    now_time = datetime.datetime.now()


    # INSERT INTO patient_info table;
    db_patient = crud.create_patient(db, Patient.PatientCreate(patient_id=patient_id, record_id=record_id, sensor_num=sensor_num))

    # INSERT INTO Time_Record table;
    db_timerecord = crud.create_timerecord(db, TimeRecord.TimeRecordCreate(record_id=record_id, last_update=now_time, doctor_id=0)) # for Dr.Lei
    db_timerecord = crud.create_timerecord(db, TimeRecord.TimeRecordCreate(record_id=record_id, last_update=now_time, doctor_id=1)) # for Dr.Liang
    db_timerecord = crud.create_timerecord(db, TimeRecord.TimeRecordCreate(record_id=record_id, last_update=now_time, doctor_id=-1))# for MMS

    # INSERT INTO raw_data table
    db_rawdata = crud.create_rawdata(db, Rawdata.RawDataCreate(filename=filename, record_id=record_id))

    # INSERT INTO ws10 with doctor_id = [0,1,-1] 
    temp = ["" for i in range(10)]
    for i in [0, 1, -1]:
        db_ws10 = crud.create_ws10(db, WetSwallow.WetSwallowCreate(record_id=record_id, vigors=temp, patterns=temp, dcis=temp, swallow_types=temp, irp4s=temp, dls=temp, doctor_id=i))
    # db_ws10 = crud.create_ws10(db, WetSwallow.WetSwallowCreate(record_id=record_id, doctor_id=0))
    # db_ws10 = crud.create_ws10(db, WetSwallow.WetSwallowCreate(record_id=record_id, doctor_id=1))
    # db_ws10 = crud.create_ws10(db, WetSwallow.WetSwallowCreate(record_id=record_id, doctor_id=-1))

    # INSERT INTO MRS with doctor_id = [0,1,-1]
    db_mrs = crud.create_mrs(db, MRS.MrsCreate(record_id=record_id, doctor_id=0))
    db_mrs = crud.create_mrs(db, MRS.MrsCreate(record_id=record_id, doctor_id=1))
    db_mrs = crud.create_mrs(db, MRS.MrsCreate(record_id=record_id, doctor_id=-1))

    # INSERT INTO Hiatal Hernia with doctor_id = [0,1,-1]
    db_hh = crud.create_hh(db, HiatalHernia.HiatalHerniaCreate(record_id=record_id, doctor_id=0))
    db_hh = crud.create_hh(db, HiatalHernia.HiatalHerniaCreate(record_id=record_id, doctor_id=1))
    db_hh = crud.create_hh(db, HiatalHernia.HiatalHerniaCreate(record_id=record_id, doctor_id=-1))


    return{
        "status":"success",
    }



