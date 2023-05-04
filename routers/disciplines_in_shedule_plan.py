from fastapi import APIRouter,  Depends, HTTPException
from shemas import *
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from db.models import disciplines_in_shedule_plan_table
from db.init import database
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

shedule_plan_disciplines_router = APIRouter (
    responses={404: {"description": "Not found"}})


#JSONResponse(status_code=404, content = {"description": "Not found","request_date":datetime.datetime.now().timestamp()
@shedule_plan_disciplines_router.post("/shedule/plan/discipline/create/", summary="Добавить новую дисциплину")
async def create(item: DisciplinesInShedulePlan) -> DisciplinesInShedulePlan:
    query = disciplines_in_shedule_plan_table.insert().values(
        name = item.name,
        hours = item.hours,
        zet = item.zet,
        education_form = item.education_form
    )
    await database.execute(query) 
    return item

@shedule_plan_disciplines_router.get("/shedule/plan/discipline/", summary="Получить данные дисциплины")
async def get_shedule_plan(id) -> DisciplinesInShedulePlan:
    query = disciplines_in_shedule_plan_table.select().where(disciplines_in_shedule_plan_table.c.id == id) 
    return await database.fetch_one(query)
    
@shedule_plan_disciplines_router.get("/shedule/plan/disciplines/", summary="Получить данные дисциплины")
async def get_shedule_plan() ->List[DisciplinesInShedulePlan]: 
    query = disciplines_in_shedule_plan_table.select()
    return await database.fetch_all(query)

@shedule_plan_disciplines_router.patch("/shedule/plan/discipline/path/", summary="Обновить данные дисциплины")
async def path_shedule_plan(item: DisciplinesInShedulePlan) -> DisciplinesInShedulePlan:
    query = disciplines_in_shedule_plan_table.udate().values(
        name = item.name,
        hours = item.hours,
        zet = item.zet,
        education_form = item.education_form
        ).where(disciplines_in_shedule_plan_table.c.id == id) 

    await database.execute(query)
    return item
   
@shedule_plan_disciplines_router.delete("/shedule/plan/discipline/delete/", summary="Удалить дисциплину")
async def delete_shedule_plan(id) -> DisciplinesInShedulePlan: 
    return DisciplinesInShedulePlan


