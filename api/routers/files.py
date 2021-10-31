from fastapi import APIRouter, Request, Form, File, UploadFile, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from utils import save_file, process_10swallow, preprocess_csv
from models.Rawdata import WsData 
from io import StringIO
from db_model.database import SessionLocal, engine # important
from models import Patient, WetSwallow
import shutil, copy, uuid
import pandas as pd 
import crud 

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

    """
    TODO:
        insert this file to DB  
    """

    # save csv file 
    # df = pd.read_csv(StringIO(str(files.file.read(), 'big5')), encoding='big5', skiprows=6)
    # filename = files.filename
    # raw_data_string, swallow_index, sensor_num = preprocess_csv(df)
    # save_file("./data/", filename, df)

    id = uuid.uuid4()
    patient_id = "A123456789"
    sensor_num = 25 


    # INSERT INTO patient_info table;
    """
    TODO:
        check this patient already in Database ?
    """
    db_patient = crud.create_patient(db, Patient.PatientCreate(patient_id=patient_id, id=id, sensor_num=sensor_num))
    print(db_patient.patient_id)
    # INSERT INTO raw_data table 

    # INSERT INTO ws10 with doctor_id = [0,1,-1] 
    db_ws10 = crud.create_ws10(db, WetSwallow.WetSwallowCreate(id=id, doctor_id=0))
    db_ws10 = crud.create_ws10(db, WetSwallow.WetSwallowCreate(id=id, doctor_id=1))
    db_ws10 = crud.create_ws10(db, WetSwallow.WetSwallowCreate(id=id, doctor_id=-1))


    return{
        "status":"success",
        "patient":db_patient,
        "ws10":db_ws10
    }



