from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4 

'''
Response or Request format 
'''
class MrsBase(BaseModel):
    record_id: UUID = Field(default_factory=uuid4)

class MrsCreate(MrsBase):
    doctor_id: int

# Come from FrontEnd
class MrsUpdate(MrsBase):
    mrs_dci_position: List
    mrs_dci: List
    dci_after_mrs_position: List
    dci_after_mrs: List 
    irp1_position: List
    irp1: List
    doctor_id: int 
    mrs_result: str = None 
    pressure_max: Optional[int]
    pressure_min: Optional[int]

class MrsGetResponse(MrsBase):
    mrs_dci_position: List
    mrs_dci: List
    dci_after_mrs_position: List
    dci_after_mrs: List 
    irp1_position: List
    irp1: List
    doctor_id: int 
    mrs_result: str
    pressure_max: Optional[int]
    pressure_min: Optional[int]
