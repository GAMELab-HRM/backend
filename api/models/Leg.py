from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic import Json
from uuid import UUID, uuid4 

'''
Response or Request format 
'''
class LegBase(BaseModel):
    record_id: UUID = Field(default_factory=uuid4)

class LegCreate(LegBase):
    doctor_id: int
    leg_metric: dict 
    draw_info: dict


    