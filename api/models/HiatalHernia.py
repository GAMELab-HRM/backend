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
