from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic import Json
from uuid import UUID, uuid4 

'''
Response or Request format 
'''
class AirBase(BaseModel):
    record_id: UUID = Field(default_factory=uuid4)

class AirCreate(AirBase):
    doctor_id: int
    air_metric: dict 



