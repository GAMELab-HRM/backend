from pydantic import BaseModel, Field
from uuid import UUID, uuid4 

class Persontest(BaseModel):
    ID: str # 身份證字號
    Name:str

