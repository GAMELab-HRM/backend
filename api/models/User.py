from lib2to3.pytree import Base
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4 

'''
Response or Request format 
'''
class UserLoginSchema(BaseModel):
    username: str 
    password: str 
