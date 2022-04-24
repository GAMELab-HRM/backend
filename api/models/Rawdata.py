from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4 

class RawDataclass(BaseModel):
    data:str

# for 10 wet swallows raw data
class WsData(BaseModel):
    filename: str
    raw: str # raw data 
    index: List[int] # index of swallow 1 ~ 10   
    sensors: int

class RawDataBase(BaseModel):
    record_id: UUID = Field(default_factory=uuid4)

class RawDataCreate(RawDataBase):
    filename: str 
    index: Optional[int]
    all_raw: Optional[List]
    ws_10_raw: Optional[List]
    ws_10_index: Optional[List]
    mrs_raw: Optional[List]
    mrs_index: Optional[List]
    rdc_raw: Optional[List]
    rdc_index: Optional[List]
    hh_raw: Optional[List]
    hh_index: Optional[List]
    leg_raw: Optional[List]
    leg_index: Optional[List]
    resting_raw: Optional[List]
    resting_index: Optional[List]
