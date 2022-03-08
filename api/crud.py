from numpy import record
from sqlalchemy.orm import Session 
import db_model.models as dbmodels 
from models import Patient, Rawdata, WetSwallow, TimeRecord, MRS, HiatalHernia, Leg, Air
from uuid import UUID, uuid4 
import pickle

"""
CRUD for raw data 
"""
def create_rawdata(db: Session, data: Rawdata.RawDataCreate):
    swallow_list_binary = pickle.dumps(data.ws_10_raw)
    mrs_list_binary = pickle.dumps(data.mrs_raw)
    hh_list_binary = pickle.dumps(data.hh_raw)
    leg_list_binary = pickle.dumps(data.leg_raw)
    all_raw_binary = pickle.dumps(data.all_raw)
    db_rawdata = dbmodels.Raw_Data(filename=data.filename, record_id=data.record_id, 
        hh_raw=hh_list_binary, ws_10_raw=swallow_list_binary, mrs_raw=mrs_list_binary, leg_raw=leg_list_binary, all_raw=all_raw_binary, 
        ws_10_index=data.ws_10_index, mrs_index=data.mrs_index, hh_index=data.hh_index, leg_index=data.leg_index)
    db.add(db_rawdata)
    db.commit()
    db.refresh(db_rawdata)
    return db_rawdata

def get_ws_rawdata(db: Session, record_id):
    ans = db.query(dbmodels.Raw_Data).filter(
        (dbmodels.Raw_Data.record_id==record_id)
    ).all()
    return ans

def get_mrs_rawdata(db: Session, record_id):
    ans = db.query(dbmodels.Raw_Data).filter(
        (dbmodels.Raw_Data.record_id==record_id)
    ).all()
    return ans

def get_hh_rawdata(db: Session, record_id):
    ans = db.query(dbmodels.Raw_Data.hh_raw).filter(
        (dbmodels.Raw_Data.record_id==record_id)
    ).all()
    return ans     

def get_leg_rawdata(db: Session, record_id):
    ans = db.query(dbmodels.Raw_Data.leg_raw).filter(
        (dbmodels.Raw_Data.record_id==record_id)
    ).all()
    return ans 

"""
CRUD for patient 
"""
def get_patients(db: Session, skip: int=0,):
    ans = db.query(dbmodels.Patient_info).offset(skip).all()
    return ans

def get_patient(): # get one patient by record_id & doctor_id
    pass

def get_catheter(record_id: UUID, db: Session):
    ans = db.query(dbmodels.Patient_info.catheter_type).filter(
        (dbmodels.Patient_info.record_id == record_id)
    ).one()
    return ans 

def create_patient(db: Session, info: Patient.PatientCreate):
    db_patient = dbmodels.Patient_info(record_id=info.record_id, patient_id=info.patient_id, catheter_type=info.catheter_type)
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

def delete_patient(db: Session, record_id):
    patient = db.query(dbmodels.Patient_info).filter(dbmodels.Patient_info.record_id==record_id).first()
    db.delete(patient)
    db.commit()
    return True 

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
    db_mrs = dbmodels.Mrs(record_id=mrs_data.record_id, doctor_id=mrs_data.doctor_id, mrs_metric=mrs_data.mrs_metric, draw_info=mrs_data.draw_info)
    db.add(db_mrs)
    db.commit()
    db.refresh(db_mrs)
    return db_mrs 

def update_mrs(db: Session, data):
    updated_mrs = db.query(dbmodels.Mrs).filter(
        (dbmodels.Mrs.record_id==data["record_id"]) & (dbmodels.Mrs.doctor_id==data["doctor_id"])
    ).update(data)
    db.commit()
    db.flush()
    return updated_mrs

def update_mrs_metric(db: Session, mrs_metric, record_id, doctor_id):
    updated_mrs = db.query(dbmodels.Mrs).filter(
        (dbmodels.Mrs.record_id == record_id) & (dbmodels.Mrs.doctor_id == doctor_id)
    ).update({"mrs_metric":mrs_metric})
    db.commit()
    db.flush()
    return updated_mrs

def update_mrs_drawinfo(db: Session, mrs_draw_data, record_id, doctor_id):
    updated_mrs = db.query(dbmodels.Mrs).filter(
        (dbmodels.Mrs.record_id == record_id) & (dbmodels.Mrs.doctor_id == doctor_id)
    ).update({"draw_info":mrs_draw_data})
    db.commit()
    db.flush()
    return updated_mrs

def update_mrs_result(db: Session, mrs_result_data, record_id, doctor_id):
    updated_mrs_result = db.query(dbmodels.Mrs).filter(
        (dbmodels.Mrs.record_id == record_id) & (dbmodels.Mrs.doctor_id == doctor_id)
    ).update(mrs_result_data)
    db.commit()
    db.flush()
    return updated_mrs_result

def get_mrs(db: Session, record_id, doctor_id):
    ans = db.query(dbmodels.Mrs).filter(
        (dbmodels.Mrs.record_id==record_id) & (dbmodels.Mrs.doctor_id==doctor_id)
    ).all()
    return ans

def get_mrs_metric(db: Session, record_id, doctor_id):
    ans = db.query(dbmodels.Mrs.mrs_metric).filter(
        (dbmodels.Mrs.record_id==record_id) & (dbmodels.Mrs.doctor_id==doctor_id)
    ).all()
    return ans[0].mrs_metric 
    
def get_mrs_drawinfo(db: Session, record_id, doctor_id):
    mrs_drawinfo = db.query(dbmodels.Mrs.draw_info).filter(
        (dbmodels.Mrs.record_id == record_id) & (dbmodels.Mrs.doctor_id == doctor_id)       
    ).all()
    return mrs_drawinfo[0].draw_info

def get_mrs_result(db: Session, record_id, doctor_id):
    mrs_result = db.query(dbmodels.Mrs.mrs_result).filter(
        (dbmodels.Mrs.record_id == record_id) & (dbmodels.Mrs.doctor_id == doctor_id)  
    ).all()
    return mrs_result[0].mrs_result
"""
CRUD for Hiatal Hernia
"""
def create_hh(db: Session, hh_data:HiatalHernia.HiatalHerniaCreate):
    db_hh = dbmodels.Hiatal_Hernia(record_id=hh_data.record_id, doctor_id=hh_data.doctor_id, hh_metric=hh_data.hh_metric, draw_info=hh_data.draw_info)
    db.add(db_hh)
    db.commit()
    db.refresh(db_hh)
    return db_hh

def get_hh_metric(db: Session, record_id, doctor_id):
    ans = db.query(dbmodels.Hiatal_Hernia.hh_metric).filter(
        (dbmodels.Hiatal_Hernia.record_id==record_id) & (dbmodels.Hiatal_Hernia.doctor_id==doctor_id)
    ).all()
    return ans[0].hh_metric 

def get_hh_drawinfo(db: Session, record_id, doctor_id):
    hh_drawinfo = db.query(dbmodels.Hiatal_Hernia.draw_info).filter(
        (dbmodels.Hiatal_Hernia.record_id == record_id) & (dbmodels.Hiatal_Hernia.doctor_id == doctor_id)       
    ).all()
    return hh_drawinfo[0].draw_info

def get_hh_reesult(db: Session, record_id, doctor_id):
    hh_result = db.query(dbmodels.Hiatal_Hernia.hiatal_hernia_result, dbmodels.Hiatal_Hernia.rip_result).filter(
        (dbmodels.Hiatal_Hernia.record_id == record_id) & (dbmodels.Hiatal_Hernia.doctor_id == doctor_id)      
    ).all()
    return hh_result[0].hiatal_hernia_result, hh_result[0].rip_result

def update_hh_metric(db: Session, hh_metric, record_id, doctor_id):
    updated_hh = db.query(dbmodels.Hiatal_Hernia).filter(
        (dbmodels.Hiatal_Hernia.record_id == record_id) & (dbmodels.Hiatal_Hernia.doctor_id == doctor_id)
    ).update({"hh_metric":hh_metric})
    db.commit()
    db.flush()
    return updated_hh

def update_hh_drawinfo(db: Session, hh_draw_data, record_id, doctor_id):
    updated_hh = db.query(dbmodels.Hiatal_Hernia).filter(
        (dbmodels.Hiatal_Hernia.record_id == record_id) & (dbmodels.Hiatal_Hernia.doctor_id == doctor_id)
    ).update({"draw_info":hh_draw_data})
    db.commit()
    db.flush()
    return updated_hh

def update_hh_result(db: Session, hh_result, record_id, doctor_id):
    updated_hh = db.query(dbmodels.Hiatal_Hernia).filter(
        (dbmodels.Hiatal_Hernia.record_id == record_id) & (dbmodels.Hiatal_Hernia.doctor_id == doctor_id)
    ).update(hh_result)
    db.commit()
    db.flush()
    return updated_hh

"""
CRUD for Air
"""
def create_air(db: Session, air_data:Air.AirCreate):
    db_air = dbmodels.Air(record_id=air_data.record_id, doctor_id=air_data.doctor_id, air_metric=air_data.air_metric)
    db.add(db_air)
    db.commit()
    db.refresh(db_air)
    return db_air

def get_air_metric(db: Session, record_id, doctor_id):
    ans = db.query(dbmodels.Air.air_metric).filter(
        (dbmodels.Air.record_id==record_id) & (dbmodels.Air.doctor_id==doctor_id)
    ).all()
    return ans[0].air_metric 

def update_air_metric(db: Session, air_metric, record_id, doctor_id):
    updated_air = db.query(dbmodels.Air).filter(
        (dbmodels.Air.record_id == record_id) & (dbmodels.Air.doctor_id == doctor_id)
    ).update({"air_metric":air_metric})
    db.commit()
    db.flush()
    return updated_air

"""
CRUD for Leg
"""
def create_leg(db: Session, leg_data:Leg.LegCreate):
    db_leg = dbmodels.Leg(record_id=leg_data.record_id, doctor_id=leg_data.doctor_id, leg_metric=leg_data.leg_metric, draw_info=leg_data.draw_info)
    db.add(db_leg)
    db.commit()
    db.refresh(db_leg)
    return db_leg

def get_leg_metric(db: Session, record_id, doctor_id):
    ans = db.query(dbmodels.Leg.leg_metric).filter(
        (dbmodels.Leg.record_id==record_id) & (dbmodels.Leg.doctor_id==doctor_id)
    ).all()
    return ans[0].leg_metric 

def get_leg_drawinfo(db: Session, record_id, doctor_id):
    leg_drawinfo = db.query(dbmodels.Leg.draw_info).filter(
        (dbmodels.Leg.record_id == record_id) & (dbmodels.Leg.doctor_id == doctor_id)       
    ).all()
    return leg_drawinfo[0].draw_info

def get_leg_reesult(db: Session, record_id, doctor_id):
    leg_result = db.query(dbmodels.Leg.leg_result).filter(
        (dbmodels.Leg.record_id == record_id) & (dbmodels.Leg.doctor_id == doctor_id)      
    ).all()
    return leg_result[0].leg_result

def update_leg_metric(db: Session, leg_metric, record_id, doctor_id):
    updated_leg = db.query(dbmodels.Leg).filter(
        (dbmodels.Leg.record_id == record_id) & (dbmodels.Leg.doctor_id == doctor_id)
    ).update({"leg_metric":leg_metric})
    db.commit()
    db.flush()
    return updated_leg

def update_leg_drawinfo(db: Session, leg_draw_data, record_id, doctor_id):
    updated_leg = db.query(dbmodels.Leg).filter(
        (dbmodels.Leg.record_id == record_id) & (dbmodels.Leg.doctor_id == doctor_id)
    ).update({"draw_info":leg_draw_data})
    db.commit()
    db.flush()
    return updated_leg

def update_leg_result(db: Session, leg_result, record_id, doctor_id):
    updated_leg = db.query(dbmodels.Leg).filter(
        (dbmodels.Leg.record_id == record_id) & (dbmodels.Leg.doctor_id == doctor_id)
    ).update(leg_result)
    db.commit()
    db.flush()
    return updated_leg


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


"""
CRUD for demoing
"""
def create_json(db: Session, info):
    db_json = dbmodels.Testing(
        draw_info=info, 
    )
    db.add(db_json)
    db.commit()
    db.refresh(db_json)
    return db_json

def get_json(db: Session):
    ans = db.query(dbmodels.Testing.draw_info).all()
    return ans 

"""
CRUD for Auth User
"""
def user_in_db(db: Session, username, password):
    user = db.query(dbmodels.User_Record).filter(
        (dbmodels.User_Record.username == username) & (dbmodels.User_Record.password == password)
    ).all()
    return user 
