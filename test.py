from fastapi import FastAPI, APIRouter
test_router = APIRouter()
from shemas import *
from mock_data import *


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