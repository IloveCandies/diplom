from fastapi import APIRouter,  Depends, HTTPException
from shemas import *
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

university_staff_router = APIRouter (
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}})


@university_staff_router.get("/university/staff/", summary="Получить данные об  сотруднике")
async def get_student_education(staff_id) -> UniversityStaff: 
    return UniversityStaff

@university_staff_router.patch("/university/staff/path/", summary="Обновить данные  сотрудникае")
async def path_student_education(staff_id) -> UniversityStaff: 
    return UniversityStaff
   
@university_staff_router.delete("/university/staff/", summary="Удалить сотрудника")
async def delete_student_education(staff_id) -> UniversityStaff: 
    return UniversityStaff
