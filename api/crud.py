from sqlalchemy.orm import Session 
from db_model import models 
from models import Patient, HRMdata, Rawdata 
from uuid import UUID, uuid4 

def get_patients(db: Session, skip: int=0,):
    return db.query(models.Patient).offset(skip).all()

def create_patient(db: Session, info: Patient.PatientCreate):
    db_patient = models.Patient(id=info.id, patient_id=info.patient_id, sensor_num=info.sensor_num)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    """
    應該要自動去wet_10、mrs、hiatal hernia新建資料(空)
    """
    return db_patient