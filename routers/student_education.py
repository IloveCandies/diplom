from fastapi import APIRouter,  Depends, HTTPException
from shemas import *
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

student_education_router = APIRouter (
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}})


#JSONResponse(status_code=404, content = {"description": "Not found","request_date":datetime.datetime.now().timestamp()
@student_education_router.post("/api/v1/education/add/", summary="Добавить образование студента")
async def add_student_education() -> StudentEducation: 
    return StudentEducation

@student_education_router.get("/api/v1/education/", summary="Получить данные об образовании студента")
async def get_student_education(student_id) -> StudentEducation: 
    return StudentEducation

@student_education_router.patch("/api/v1/education/path/", summary="Обновить данные данные об образовании студента")
async def path_student_education(student_id) -> StudentEducation: 
    return StudentEducation
   
@student_education_router.delete("/api/v1/student/education/discipline/delete/", summary="Удалить образование студента")
async def delete_student_education(student_id) -> StudentEducation: 
    return StudentEducation

