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
