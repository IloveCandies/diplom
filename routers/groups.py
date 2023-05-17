from fastapi import APIRouter,Security
from asyncpg import exceptions
from mock_data import *
from shemas import *
from db.models import group_table
from db.init import database
from fastapi.responses import JSONResponse
from middleware.jwt import *


group_router = APIRouter(responses= {400: {"detail":{"datetime": datetime.datetime.now(),"msg": "string"}}})

@group_router.post("/group/create/", summary="Добавить новую группу  тут пока нет года окончания и плана, добавлю  как готово будет")
async def add_group(item: Group) -> Group: 
    query = group_table.insert().values(
        name = item.name, year_of_recruitment = item.year_of_recruitment,
        available_places = item.available_places, potential_places = item.potential_places,
        course = item.course, end_year = item.end_year)
    try:
        await database.execute(query)
    except (exceptions.UniqueViolationError):
        return JSONResponse(status_code=400, content = {"detail":
        {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
        "msg": "Группа с таким именем уже существует "}})
    return item

@group_router.get("/group/", summary="Получить данные конкретной группы по id")
async def get_group(group_id:int) -> Group: 
    query  = group_table.select().where(group_table.c.id == group_id)
    return await database.fetch_one(query)

@group_router.get("/groups/", summary="Получить данные всех групп")
async def get_groups() -> List[Group]: 
    query = group_table.select()
    return await database.fetch_all(query)

@group_router.get("/groups/test-token/", summary="Получить данные всех групп | ТЕСТ ЗАПРОСА ТОКЕНА")
async def get_groups(token:JwtAuthorizationCredentials = Security(access_security)) -> List[Group]: 
    query = group_table.select()
    return await database.fetch_all(query)
#подумать как делать
@group_router.post("/group/add/plan/", summary="Добавить план в группу  НЕ ДОДЕЛАННО")
async def add_shedule_plan(shedule_plan_id:int) -> Group: 
    return GroupTableRecord


@group_router.post("/group/detail/", summary="Детали группы НЕ ДОДЕЛАННО")
async def add_group(item: Group) -> GroupDetail: 
    return item

@group_router.patch("/group/path/", summary="Обновить данные группы, взятой по id  НЕ СДЕЛАННО")
async def path_group(id): 
    return False
   
@group_router.delete("/group/delete/", summary="Удалить групу, взятую по id  НЕ СДЕЛАННО")
async def delete_group(id) -> Group: 
    return Group

