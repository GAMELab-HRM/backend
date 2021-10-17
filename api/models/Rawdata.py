from pydantic import BaseModel
from typing import List
class RawDataclass(BaseModel):
    data:str

# for 10 wet swallows raw data
class WsData(BaseModel):
    filename: str
    raw: str # raw data 
    index: List[int] # index of swallow 1 ~ 10   
    sensors: int
# for MRS raw data
class MrsData(BaseModel):
    pass 

# for RDC raw data 
class RdcData(BaseModel):
    pass 

# for Hiatal hernia raw data 
class HhData(BaseModel):
    pass 
