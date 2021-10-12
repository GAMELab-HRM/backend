from fastapi import APIRouter 
from fastapi import Request, Form, File ,UploadFile
from utils import save_file, process_10swallow
from models.HRMdata import CustomClass, HRMclass
import shutil


router = APIRouter(
    prefix="/api/v1/swallows",
    tags=["10 wet swallows"]
)


@router.get("/data")
def get_swallow_data():
    return{"msg":"Hello swallow datas"}

@router.post("/data")
def add_swallow_data(data:CustomClass):
    process_10swallow(data.GT)
    process_10swallow(data.MMS)
    return {"msg":"add new swallow data"}

# upload 10 wet swallows csv 
@router.post("/file")
def upload_swallow_file(request:Request, files: UploadFile = File(...)):
    save_file("./data/wet_swallows/", files)
    return {
        "file size": 0,
        "file name": files.filename
    }
  


