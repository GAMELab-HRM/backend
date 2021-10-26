from typing import List 
from pydantic import BaseModel, Field
from uuid import UUID, uuid4 

'''
Response or Request format 
'''
class PatientBase(BaseModel):
    patient_id: str

class PatientCreate(PatientBase):
    id: UUID = Field(default_factory=uuid4)
    sensor_num:int 

class PatientRow(PatientBase):
    filename: str 
    doctor_id: str
    ws_10_result: str
    mrs_result: str
    hiatal_hernia_result: str
    rip_result: str
    last_update: str