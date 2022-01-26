from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4 

'''
Response or Request format 
'''
class WetSwallowBase(BaseModel):
    record_id: UUID = Field(default_factory=uuid4)

class WetSwallowCreate(WetSwallowBase):
    vigors: Optional[List]
    patterns: Optional[List] 
    dcis: Optional[List] 
    swallow_types: Optional[List] 
    irp4s: Optional[List] 
    dls: Optional[List] 
    doctor_id: int
    pressure_max: Optional[int]
    pressure_min: Optional[int] 

# Come from FrontEnd
class WetSwallowUpdate(WetSwallowBase):
    vigors: List
    patterns: List 
    dcis: List 
    breaks: List
    swallow_types: List 
    irp4s: List 
    dls: List 
    doctor_id: int 
    ws_result: str 
    pressure_max: Optional[int]
    pressure_min: Optional[int] 

class WetSwallowGet(WetSwallowBase):
    doctor_id: int

class WetSwallowGetResponse(WetSwallowBase):
    vigors: List
    patterns: List 
    dcis: List 
    breaks: List
    swallow_types: List 
    irp4s: List 
    dls: List 
    doctor_id: int 
    ws_result: str = None 
    pressure_max: Optional[int]
    pressure_min: Optional[int] 