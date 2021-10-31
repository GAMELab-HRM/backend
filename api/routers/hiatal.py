from fastapi import APIRouter 
from fastapi import Request, Form, File ,UploadFile
from utils import save_file
import shutil

router = APIRouter(
    prefix="/api/v1/hiatal",
    tags=["Hiatal hernia"]
)

@router.get("/data")
def get_hiatal_data():
    return{"msg":"Hello hiatal datas"}

@router.post("/data")
def add_hiatal_data():
    return {"msg":"add hiatal data"}

@router.put("/data")
def update_hiatal_data():
    return {"msg":"update hiatal data"}

