from fastapi import APIRouter
from shemas import *

shedule_plan_router = APIRouter()

@shedule_plan_router.post("/shedule/plan/add/", summary="Добавить новый учебный план")
async def add_shedule_plan() -> ShedulePlan: 
    return ShedulePlan

@shedule_plan_router.post("/shedule/plan/add/discipline/", summary="Добавить в учебный план дисциплину")
async def add_shedule_plan(id) -> ShedulePlan: 
    return ShedulePlan

@shedule_plan_router.get("/shedule/plan/", summary="Получить данные конкретного плана")
async def get_shedule_plan(id) -> ShedulePlan: 
    return ShedulePlan 

@shedule_plan_router.get("/shedule/plans/", summary="Получить данные всех учебных планов")
async def get_shedule_plans() -> List[ShedulePlan]: 
    return List[ShedulePlan]


@shedule_plan_router.patch("/shedule/plan/path/", summary="Обновить данные учебного плана")
async def path_shedule_plan(id) -> ShedulePlan: 
    return ShedulePlan

@shedule_plan_router.delete("/shedule/plan/delete/", summary="Удалить план")
async def delete_shedule_plan(id) -> ShedulePlan: 
    return ShedulePlan

