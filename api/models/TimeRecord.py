from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4 

'''
Response or Request format 
'''
class TimeRecordBase(BaseModel):
    record_id: UUID = Field(default_factory=uuid4)

class TimeRecordCreate(TimeRecordBase):
    doctor_id: int
    last_update: Optional[datetime]
