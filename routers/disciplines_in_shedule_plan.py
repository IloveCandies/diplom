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
@shedule_plan_disciplines_router.post("/api/v1/shedule/plan/discipline/create/", summary="Добавить новую дисциплину")
async def create(item: DisciplinesInShedulePlan) -> DisciplinesInShedulePlan:
    query = disciplines_in_shedule_plan_table.insert().values(
        hours = item.hours,
        zet = item.zet,
    )
    await database.execute(query) 
    return item

@shedule_plan_disciplines_router.get("/api/v1/shedule/plan/discipline/", summary="Получить данные дисциплины")
async def get_shedule_plan(id:int) -> DisciplinesInShedulePlan:
    query = disciplines_in_shedule_plan_table.select().where(disciplines_in_shedule_plan_table.c.id == id) 
    return await database.fetch_one(query)
    
@shedule_plan_disciplines_router.get("/api/v1/shedule/plan/disciplines/", summary="Получить данные дисциплины")
async def get_shedule_plan() ->List[DisciplinesInShedulePlan]: 
    query = disciplines_in_shedule_plan_table.select()
    return await database.fetch_all(query)

@shedule_plan_disciplines_router.patch("/api/v1/shedule/plan/discipline/path/", summary="Обновить данные дисциплины")
async def path_shedule_plan(item: DisciplinesInShedulePlan, discipline_in_plan_id:int) -> DisciplinesInShedulePlan:
    query = disciplines_in_shedule_plan_table.update().values(
        hours = item.hours,
        zet = item.zet
        ).where(disciplines_in_shedule_plan_table.c.id == discipline_in_plan_id) 

    await database.execute(query)
    return item
   
@shedule_plan_disciplines_router.delete("/api/v1/shedule/plan/discipline/delete/", summary="Удалить дисциплину")
async def delete_shedule_plan(id) -> DisciplinesInShedulePlan: 
    return DisciplinesInShedulePlan


