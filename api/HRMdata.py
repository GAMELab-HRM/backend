from pydantic import BaseModel
class HRMclass(BaseModel):
    id: str # 身份證字號
    vigor: list # contraction vigor
    pattern: list # contraction pattern 
    swallow_type: str # swallow type 
    irp: list # IRP4
    dci: list # DCI