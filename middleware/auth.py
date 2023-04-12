from fastapi import APIRouter
from mock_data import *
from shemas import *

router = APIRouter()

@router.get("/login/")
async def login(email:str,password:str) -> Student :
    print(Students)
    for student in Students:
        #хэш анхэш
        if (student.email == email) and (student.password == password):
            return student
