from sqlalchemy.orm import Session 
import db_model.models as dbmodels 
from models import Patient, Rawdata, WetSwallow, TimeRecord, MRS, HiatalHernia
from uuid import UUID, uuid4 
import pickle
"""
CRUD for raw data 
"""
def create_rawdata(db: Session, data: Rawdata.RawDataCreate):
    db_rawdata = dbmodels.Raw_Data(filename=data.filename, record_id=data.record_id)
    db.add(db_rawdata)
    db.commit()
    db.refresh(db_rawdata)
    return db_rawdata

"""
CRUD for patient 
"""
def get_patients(db: Session, skip: int=0,):
    ans = db.query(dbmodels.Patient_info).offset(skip).all()
    return ans

def get_patient(): # get one patient by record_id & doctor_id
    pass
def create_patient(db: Session, info: Patient.PatientCreate):
    db_patient = dbmodels.Patient_info(record_id=info.record_id, patient_id=info.patient_id, sensor_num=info.sensor_num)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

"""
CRUD for 10 wet swallows 
"""
def get_ws10(db: Session, ws_info:WetSwallow.WetSwallowGet):
    ans = db.query(dbmodels.Wet_swallows_10).filter(
        (dbmodels.Wet_swallows_10.record_id==ws_info.record_id) & (dbmodels.Wet_swallows_10.doctor_id==ws_info.doctor_id)
    ).all()
    return ans

def update_ws10(db: Session, data):
    updated_ws10 = db.query(dbmodels.Wet_swallows_10).filter(
        (dbmodels.Wet_swallows_10.record_id==data["record_id"]) & (dbmodels.Wet_swallows_10.doctor_id==data["doctor_id"])
    ).update(data)
    db.commit()
    db.flush()
    return updated_ws10

def create_ws10(db: Session, ws_data:WetSwallow.WetSwallowCreate):
    db_ws10 = dbmodels.Wet_swallows_10(
        record_id=ws_data.record_id, 
        doctor_id=ws_data.doctor_id,
    )
    db.add(db_ws10)
    db.commit()
    db.refresh(db_ws10)
    return db_ws10

"""
CRUD for MRS 
"""
def create_mrs(db: Session, mrs_data:MRS.MrsCreate):
    db_mrs = dbmodels.Mrs(record_id=mrs_data.record_id, doctor_id=mrs_data.doctor_id)
    db.add(db_mrs)
    db.commit()
    db.refresh(db_mrs)
    return db_mrs 

"""
CRUD for Hiatal Hernia
"""
def create_hh(db: Session, hh_data:HiatalHernia.HiatalHerniaCreate):
    db_hh = dbmodels.Hiatal_Hernia(record_id=hh_data.record_id, doctor_id=hh_data.doctor_id)
    db.add(db_hh)
    db.commit()
    db.refresh(db_hh)
    return db_hh

"""
CRUD for Time Record
"""
def create_timerecord(db: Session, time_data:TimeRecord.TimeRecordCreate):
    db_timerecord = dbmodels.Time_Record(record_id=time_data.record_id, last_update=time_data.last_update, doctor_id=time_data.doctor_id)
    db.add(db_timerecord)
    db.commit()
    db.refresh(db_timerecord)
    return db_timerecord

"""
CRUD for frontend's upload Table 
"""
def get_upload_info(db: Session):
    result = db.query(
        dbmodels.Patient_info.record_id,
        dbmodels.Patient_info.patient_id, 
        dbmodels.Raw_Data.filename, 
        dbmodels.Time_Record.last_update
    ).filter(
        dbmodels.Patient_info.record_id == dbmodels.Raw_Data.record_id
    ).filter(
        dbmodels.Patient_info.record_id == dbmodels.Time_Record.record_id
    ).filter(
        dbmodels.Time_Record.doctor_id == -1
    ).all()
    return result 

def get_all_info(db: Session):
    result = db.query(
        dbmodels.Patient_info.record_id,
        dbmodels.Patient_info.patient_id,
        dbmodels.Time_Record.doctor_id,
        dbmodels.Raw_Data.filename,
        dbmodels.Time_Record.last_update,
        dbmodels.Wet_swallows_10.ws_result,
        dbmodels.Mrs.mrs_result,
        dbmodels.Hiatal_Hernia.hiatal_hernia_result,
        dbmodels.Hiatal_Hernia.rip_result
    ).filter(
        (dbmodels.Patient_info.record_id == dbmodels.Raw_Data.record_id) 
        & (dbmodels.Patient_info.record_id == dbmodels.Wet_swallows_10.record_id) 
        & (dbmodels.Patient_info.record_id == dbmodels.Time_Record.record_id)
        & (dbmodels.Patient_info.record_id == dbmodels.Mrs.record_id)
        & (dbmodels.Patient_info.record_id == dbmodels.Hiatal_Hernia.record_id)
    ).filter(
        (dbmodels.Time_Record.doctor_id == dbmodels.Wet_swallows_10.doctor_id)
        & (dbmodels.Time_Record.doctor_id == dbmodels.Mrs.doctor_id)
        & (dbmodels.Time_Record.doctor_id == dbmodels.Hiatal_Hernia.doctor_id)
    ).filter(
        (dbmodels.Time_Record.doctor_id != -1) 
        &(dbmodels.Wet_swallows_10.doctor_id != -1)
        &(dbmodels.Mrs.doctor_id != -1)
        &(dbmodels.Hiatal_Hernia.doctor_id != -1)
    ).all()
    return result 


