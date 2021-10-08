from pydantic import BaseModel
class HRMclass(BaseModel):
    ID: str # 身份證字號
    V: list # contraction vigor
    P: list # contraction pattern 
    swallow_type: list # swallow type 
    IRP40: list # IRP4
    DCI: list # DCI
    DL: list 
    cc_result: str
    doctor: str

class CustomClass(BaseModel):
    GT: HRMclass
    MMS: HRMclass