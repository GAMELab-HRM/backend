from fastapi import APIRouter, Depends
from models import WetSwallow, MRS
from models.Rawdata import WsData 
from sqlalchemy.orm import Session 
from db_model.database import SessionLocal, engine # important
from typing import Dict, Any
import crud, pickle, json
import pandas as pd 
from uuid import UUID
from auth.auth_bearer import JWTBearer 

router = APIRouter(
    prefix="/api/v1/air",
    tags=["air(二度收縮)"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()


@router.get("/metrics")
def get_air_metric(record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    air_metric = crud.get_air_metric(db, record_id, doctor_id)
    return air_metric

@router.put("/metrics")
def update_air_metric(request: Dict[Any, Any], record_id: UUID, doctor_id: int, db: Session = Depends(get_db)):
    air_metric = crud.update_air_metric(db, request, record_id, doctor_id)
    return air_metric


