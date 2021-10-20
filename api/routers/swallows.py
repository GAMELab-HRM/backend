from fastapi import APIRouter 
from fastapi import Request, Form, File ,UploadFile
from utils import save_file, process_10swallow, preprocess_csv
from models.HRMdata import CustomClass, HRMclass
from models.Rawdata import WsData 
from io import StringIO
import shutil, copy
import pandas as pd 


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

@router.put("/data")
def update_swallow_data():
    return {"msg":"updated"}
    
# upload 10 wet swallows csv 
@router.post("/file", response_model = WsData)
def upload_swallow_file(request:Request, files: UploadFile = File(...)):

    """
    TODO:
        check raw.csv already in Database ?
    """
    # temp_file = copy.deepcopy(files)
    df = pd.read_csv(StringIO(str(files.file.read(), 'big5')), encoding='big5', skiprows=6)
    filename = files.filename
    raw_data_string, swallow_index, sensor_num = preprocess_csv(df)
    save_file("./data/wet_swallows/", filename, df)

    return{
        "filename": filename,
        "raw": raw_data_string,
        "index": swallow_index,
        "sensors": sensor_num
    }



