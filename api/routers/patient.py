from fastapi import APIRouter 
from fastapi import Request, Form, File ,UploadFile, Depends
from typing import List
from utils import save_file
import shutil
import crud 
from sqlalchemy.orm import Session 
from db_model.database import SessionLocal, engine
from models import Patient
from uuid import UUID, uuid4

router = APIRouter(
    prefix="/api/v1/patient",
    tags=["for patient"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()

@router.get("/", response_model=List[Patient.PatientObject])
def get_patients_data(skip: int = 0, db: Session = Depends(get_db)):
    patients = crud.get_patients(db, skip=skip)
    return patients

@router.post("/")
def create_patient_data(patient_info:Patient.PatientCreate ,db: Session = Depends(get_db)):
    db_patient = crud.create_patient(db, patient_info)
    return db_patient

@router.delete("/{record_id}")
def delete_patient(record_id:UUID, db: Session = Depends(get_db)):
    deleted = crud.delete_patient(db, record_id)
    return {
        "deleted":deleted
    }

@router.get("/catheter", response_model=Patient.PatientCatheter)
def get_catheter_type(record_id: UUID, db: Session = Depends(get_db)):
    catheter_type = crud.get_catheter(record_id, db)[0]
    return {
        "record_id": record_id,
        "catheter_type": catheter_type
    }