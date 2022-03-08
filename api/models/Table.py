from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4 

'''
Response or Request format 
'''
class TableBase(BaseModel):
    record_id: UUID = Field(default_factory=uuid4)

class UploadPageTable(TableBase):
    patient_id: str
    filename: str
    last_update: datetime 

    class Config:
        orm_mode = True

# for 所有資料page
class AllTable(TableBase):
    patient_id: str 
    doctor_id: int 
    filename: str 
    last_update: datetime 
    ws_result: Optional[str] = None 
    mrs_result: Optional[str] = None 
    mrs_draw: Optional[bool] = None 
    hiatal_hernia_result: Optional[str] = None  
    hh_draw: Optional[bool] = None
    rip_result: Optional[str] = None 

    class Config:
        orm_mode = True 
