from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4 

'''
Response or Request format 
'''
class HiatalHerniaBase(BaseModel):
    record_id: UUID = Field(default_factory=uuid4)

class HiatalHerniaCreate(HiatalHerniaBase):
    doctor_id: int
    hh_metric: dict 
    draw_info: dict 

class HiatalHerniaUpdate(HiatalHerniaBase):
    les_position: List
    cd_position: List 
    rip_position: List 
    seperate: bool 
    hiatal_hernia_result: str 
    rip_result: str 
    doctor_id: int 
    pressure_max: Optional[int]
    pressure_min: Optional[int]

    
class HiatalHerniaGetResponse(HiatalHerniaBase):
    les_position: List
    cd_position: List 
    rip_position: List 
    seperate: bool 
    hiatal_hernia_result: str 
    rip_result: str 
    doctor_id: int 
    pressure_max: Optional[int]
    pressure_min: Optional[int]
    
class HiatalHerniaResult(BaseModel):
    hh_result: str
    rip_result: str 