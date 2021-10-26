from fastapi import APIRouter 
from fastapi import Request, Form, File ,UploadFile, Depends
from utils import save_file
import shutil
import crud 
from sqlalchemy.orm import Session 
from db_model.database import SessionLocal, engine
from models import Patient
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

@router.get("/")
def get_patients_data(skip: int = 0, db: Session = Depends(get_db)):
    patients = crud.get_patients(db, skip=skip)
    return patients

@router.post("/")
def create_patient_data(patient_info:Patient.PatientCreate ,db: Session = Depends(get_db)):
    db_patient = crud.create_patient(db, patient_info)
    return db_patient
