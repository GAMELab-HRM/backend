from fastapi import APIRouter, Request, Form, File, UploadFile, Depends, FastAPI, HTTPException, Response
from rsa import sign
from sqlalchemy.orm import Session
from auth.auth_handler import signJWT, signRefreshJWT, decodeJWT
from auth.auth_bearer import JWTBearer 
from utils import save_file, preprocess_csv, parsing_csv
from io import StringIO
from db_model.database import SessionLocal, engine # important
from models import User
import shutil, copy, uuid, datetime, crud, pickle
import pandas as pd 
from fastapi.security import HTTPBasicCredentials, HTTPBearer
security = HTTPBearer()

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["for user auth"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_user(data: User.UserLoginSchema,db: Session = Depends(get_db)):
    #去db比對是否有這筆資料
    pass 
@router.get("/", dependencies=[Depends(JWTBearer())])
def get_with_jwt():
    return {"status":"ok"}

@router.post("/")
def upload_swallow_file(request:Request, files: UploadFile = File(...), db: Session = Depends(get_db)):
    pass 

@router.post("/login")
def user_login(user_info: User.UserLoginSchema, db: Session = Depends(get_db)):
    query_result = crud.user_in_db(db, user_info.username, user_info.password)
    if len(query_result) == 0:
        raise HTTPException(status_code=403, detail="username or Password Error!")
    token = signJWT(user_info.username)["access_token"]
    refresh_token = signRefreshJWT(user_info.username)["refresh_token"]
    return {
        "access_token": token,
        "refresh_token": refresh_token
    }

@router.post("/refresh")
def refresh_jwt(credentials: HTTPBasicCredentials = Depends(security)):
    refresh_token = credentials.credentials
    payload = decodeJWT(refresh_token)
    if payload:
        access_token = signJWT(payload["username"])["access_token"]
        return {"access_token": access_token}
    else:
        raise HTTPException(403, detail="refresh token expired")
    