from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from routers import hiatal, swallows, mrs, rdc, patient, files, table, auth, modify
from utils import *
from typing import List 

# create app instance 
app = FastAPI()
 
# CORS 
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FastAPI router 
app.include_router(hiatal.router)
app.include_router(swallows.router)
app.include_router(mrs.router)
app.include_router(rdc.router)
app.include_router(patient.router)
app.include_router(files.router)
app.include_router(table.router)
app.include_router(auth.router)
app.include_router(modify.router)

"""
TEST endpoint
"""
@app.get("/")
def read_root():
    return {"Hello": "World"}
    