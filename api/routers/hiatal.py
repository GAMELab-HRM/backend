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

@router.post("/file")
def upload_hiatal_file(request:Request, files: UploadFile = File(...)):
    save_file("./data/hiatal_hernia/", files)
    return {
        "file size": 0,
        "file name": files.filename
    }