from fastapi import APIRouter,  Depends, HTTPException
from shemas import *
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

shedule_plan_disciplines_router = APIRouter (
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}})


#JSONResponse(status_code=404, content = {"description": "Not found","request_date":datetime.datetime.now().timestamp()
@shedule_plan_disciplines_router.post("/shedule/plan/discipline/add/", summary="Добавить новую дисциплину")
async def add_shedule_plan() -> DisciplinesInShedulePlan: 
    return DisciplinesInShedulePlan

@shedule_plan_disciplines_router.get("/shedule/plan/discipline/", summary="Получить данные дисциплины")
async def get_shedule_plan(id) -> DisciplinesInShedulePlan: 
    return DisciplinesInShedulePlan

@shedule_plan_disciplines_router.patch("/shedule/plan/discipline/path/", summary="Обновить данные дисциплины")
async def path_shedule_plan(id) -> DisciplinesInShedulePlan: 
    return DisciplinesInShedulePlan
   
@shedule_plan_disciplines_router.delete("/shedule/plan/discipline/delete/", summary="Удалить дисциплину")
async def delete_shedule_plan(id) -> DisciplinesInShedulePlan: 
    return DisciplinesInShedulePlan

@shedule_plan_disciplines_router.get("/shedule/plan/disciplines/", summary="Получить данные всех дисциплин")
async def get_shedule_plans() -> List[DisciplinesInShedulePlan]: 
    return List[DisciplinesInShedulePlan]
