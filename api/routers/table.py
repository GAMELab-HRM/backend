from fastapi import APIRouter, Request, Form, File ,UploadFile, Depends
from sqlalchemy.orm import Session
from utils import save_file
from models import Table 
from typing import List
from db_model.database import SessionLocal, engine # important
import shutil, crud

router = APIRouter(
    prefix="/api/v1/table",
    tags=["For frontend's tables"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/basic_test/upload", response_model=List[Table.UploadPageTable])
def get_basic_upload_table(db: Session = Depends(get_db)):
    result = crud.get_upload_info(db)
    return result 

@router.get("/basic_test/all", response_model=List[Table.AllTable])
def get_basic_all_table(db: Session = Depends(get_db)):
    result = crud.get_all_info(db)
    return result

