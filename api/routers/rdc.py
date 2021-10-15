from fastapi import APIRouter 
from fastapi import Request, Form, File ,UploadFile
from utils import save_file
import shutil

router = APIRouter(
    prefix="/api/v1/rdc",
    tags=["Rapid drink challenge"]
)

@router.get("/data")
def get_rdc_data():
    return{"msg":"Hello hiatal datas"}

@router.post("/data")
def add_rdc_data():
    return {"msg":"add rdc data"}

@router.put("/data")
def update_rdc_data():
    return {"msg":"rdc updated"}
    
@router.post("/file")
def upload_rdc_file(request:Request, files: UploadFile = File(...)):
    save_file("./data/hiatal_hernia/", files)
    return {
        "file size": 0,
        "file name": files.filename
    }