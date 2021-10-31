from fastapi import APIRouter 
from fastapi import Request, Form, File ,UploadFile
from utils import save_file
import shutil

router = APIRouter(
    prefix="/api/v1/mrs",
    tags=["Multiple rapid swallows"]
)

@router.get("/data")
def get_mrs_data():
    return{"msg":"Hello hiatal datas"}

@router.post("/data")
def add_mrs_data():
    return{"msg":"add mrs data"}
    
@router.put("/data")
def update_mrs_data():
    return {"msg":"update mrs data"}

