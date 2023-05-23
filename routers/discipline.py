from fastapi import APIRouter,  Depends, HTTPException
from shemas import *
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from db.models import disciplines_table
from db.init import database
from asyncpg import exceptions
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

discipline_router = APIRouter (
    responses={404: {"description": "Not found"}})


#JSONResponse(status_code=404, content = {"description": "Not found","request_date":datetime.datetime.now().timestamp()
@discipline_router.post("/api/v1/discipline/create/", summary="Добавить новую дисциплину")
async def create(discipline_name: str) -> DisciplineTableRecord:
    query = disciplines_table.insert().values(name = discipline_name)
    try:
        discipline = await database.execute(query)
    except (exceptions.UniqueViolationError):
        return JSONResponse(status_code=422, content = {"description": "Дисциплина уже существует"})
    return DisciplineTableRecord(id = discipline, name=discipline_name)

@discipline_router.get("/api/v1/discipline/", summary="Получить данные дисциплины")
async def get_dicsipline(id:int) -> DisciplineTableRecord:
    query = disciplines_table.select().where(disciplines_table.c.id == id) 
    return await database.fetch_one(query)
    
@discipline_router.get("/api/v1/disciplines/", summary="Получить данные дисциплины")
async def get_dicsiplines() ->List[DisciplineTableRecord]: 
    query = disciplines_table.select()
    return await database.fetch_all(query)
  
@discipline_router.delete("/api/v1/discipline/delete/", summary="Удалить дисциплину")
async def delete_shedule_plan(id) -> bool: 
    return True


