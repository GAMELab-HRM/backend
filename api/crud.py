from sqlalchemy.orm import Session 
import db_model.models as dbmodels 
from models import Patient, Rawdata, WetSwallow
from uuid import UUID, uuid4 

def get_patients(db: Session, skip: int=0,):
    ans = db.query(models.Patient_info).filter(models.Patient_info.patient_id == "J122971623").offset(skip).all()
    print(ans[0].id)
    print(ans[0].patient_id)
    print(ans[0].ws_data)
    # print(ans[0].ws_data)
    return ans

def create_patient(db: Session, info: Patient.PatientCreate):
    db_patient = dbmodels.Patient_info(id=info.id, patient_id=info.patient_id, sensor_num=info.sensor_num)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_ws_10(db: Session):
    pass 

def create_ws10(db: Session, ws_data:WetSwallow.WetSwallowCreate):
    db_ws10 = dbmodels.Wet_swallows_10(id=ws_data.id, doctor_id=ws_data.doctor_id)
    db.add(db_ws10)
    db.commit()
    db.refresh(db_ws10)
    return db_ws10
    
