from fastapi import APIRouter,  Depends, HTTPException
from shemas import *
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

university_staff_router = APIRouter (
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}})


#JSONResponse(status_code=404, content = {"description": "Not found","request_date":datetime.datetime.now().timestamp()
@university_staff_router.post("/university/staff/add/", summary="Добавить образование студента")
async def add_student_education() -> UniversityStaff: 
    return UniversityStaff

@university_staff_router.get("/university/staff/", summary="Получить данные об образовании студента")
async def get_student_education(staff_id) -> UniversityStaff: 
    return UniversityStaff

@university_staff_router.patch("/university/staff/path/", summary="Обновить данные данные об образовании студента")
async def path_student_education(staff_id) -> UniversityStaff: 
    return UniversityStaff
   
@university_staff_router.delete("/university/staff/", summary="Удалить образование студента")
async def delete_student_education(staff_id) -> UniversityStaff: 
    return UniversityStaff
