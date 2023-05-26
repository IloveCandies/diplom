from fastapi import APIRouter,  Depends, HTTPException
from shemas import *
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

student_education_disciplines_router = APIRouter (
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}})


#JSONResponse(status_code=404, content = {"description": "Not found","request_date":datetime.datetime.now().timestamp()
@student_education_disciplines_router.post("/student/education/discipline/add/", summary="Добавить новую дисциплину")
async def add_shedule_plan() -> DisciplinesInStudentEducation: 
    return DisciplinesInStudentEducation

@student_education_disciplines_router.get("/student/education/discipline/", summary="Получить данные дисциплины")
async def get_shedule_plan(id) -> DisciplinesInStudentEducation: 
    return DisciplinesInStudentEducation

@student_education_disciplines_router.patch("/student/education/discipline/path/", summary="Обновить данные дисциплины")
async def path_shedule_plan(id) -> DisciplinesInStudentEducation: 
    return DisciplinesInStudentEducation
   
@student_education_disciplines_router.delete("/student/education/discipline/delete/", summary="Удалить дисциплину")
async def delete_shedule_plan(id) -> DisciplinesInStudentEducation: 
    return DisciplinesInStudentEducation

@student_education_disciplines_router.get("/student/education/disciplines/", summary="Получить данные всех дисциплин")
async def get_shedule_plans() -> List[DisciplinesInStudentEducation]: 
    return List[DisciplinesInStudentEducation]
