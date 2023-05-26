from fastapi import FastAPI, APIRouter, File, UploadFile
from typing import Annotated
test_router = APIRouter()
from shemas import *


@test_router.get("/",tags=["test","qwqw"])
async def root():
    return {"message": "Hello World"}

@test_router.get("/login/",tags=["test","qwqw"])
async def login(email:str,password:str) -> Student :
    print(Students)
    for student in Students:
        #хэш анхэш
        if (student.email == email) and (student.password == password):
            return student

@test_router.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@test_router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}