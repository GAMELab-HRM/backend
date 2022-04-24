from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4 

'''
Response or Request format 
'''
class RestingBase(BaseModel):
    record_id: UUID = Field(default_factory=uuid4)

class RestingCreate(RestingBase):
    doctor_id: int
    resting_metric: dict 
    draw_info: dict 
    resting_result: List 
    rip_result: List 

class RestingUpdate(RestingBase):
    les_position: List
    cd_position: List 
    rip_position: List 
    seperate: bool 
    resting_result: List 
    rip_result: List 
    doctor_id: int 
    pressure_max: Optional[int]
    pressure_min: Optional[int]

    
class RestingGetResponse(RestingBase):
    les_position: List
    cd_position: List 
    rip_position: List 
    seperate: bool 
    resting_result: List 
    rip_result: List 
    doctor_id: int 
    pressure_max: Optional[int]
    pressure_min: Optional[int]
    
class RestingResult(BaseModel):
    resting_result: List
    rip_result: List 