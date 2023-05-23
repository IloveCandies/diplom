from fastapi import APIRouter,Security
from asyncpg import exceptions
from shemas import *
from db.models import group_table, shedule_plan_table, oop_table
from db.init import database
from fastapi.responses import JSONResponse
from middleware.jwt import *
from .oop import get_oop
from .shedule_plan import get_shedule_plan
group_router = APIRouter(responses={404: {"model": Message},400: {"model": Message}})

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
async def get_group(group_name:str) ->GroupDetail: 
    query = group_table.select().where(group_table.c.name == group_name)
    group = await database.fetch_one(query)
    shedule_plan = await get_shedule_plan(group["shedule_plan"])
    print(shedule_plan)
    return {
            "name":group["name"],
            "year_of_recruitment":group["year_of_recruitment"],
            "available_places":group["available_places"],
            "potential_places":group["potential_places"],
            "course":group["course"], "end_year":group["end_year"],
            "shedule_plan":shedule_plan}

async def get_group_by_id(id:int) ->GroupDetail: 
    query = group_table.select().where(group_table.c.id == id)
    group = await database.fetch_one(query)
    shedule_plan = await get_shedule_plan(group["shedule_plan"])
    return {
            "name":group["name"],
            "year_of_recruitment":group["year_of_recruitment"],
            "available_places":group["available_places"],
            "potential_places":group["potential_places"],
            "course":group["course"], "end_year":group["end_year"],
            "shedule_plan":shedule_plan}


@group_router.get("/groups/", summary="Получить данные всех групп")
async def get_groups() -> List[GroupDetail]: 
    query = group_table.select()
    groups = await database.fetch_all(query)
    print(groups)
    detailed_groups = []
    for group in groups:
        group_detail = await get_group(group["name"])
        detailed_groups.append(group_detail)
    return detailed_groups
    
@group_router.post("/group/add/plan", summary="Добавить учебный план в группу")
async def add_plan(shedule_plan_code:str, group_name:str) -> GroupDetail: 
    query = shedule_plan_table.select().where(shedule_plan_table.c.code == shedule_plan_code)
    shedule_plan = await database.fetch_one(query)
    query = group_table.update().values(shedule_plan = shedule_plan["id"]).where(group_table.c.name == group_name)
    
    if shedule_plan == None:
        return JSONResponse(status_code=422, content = {"description": "Учебный план не существует чтобы создать дисциплину воспользуйтесь методом /disciplines/create/"})
    await database.execute(query)

    query = group_table.select().where(group_table.c.name == group_name)
    group = await database.fetch_one(query)
    query = oop_table.select().where(oop_table.c.id == shedule_plan["oop"])
    oop_detail = await  database.fetch_one(query)
    shedule_plan_detail = ShedulePlan(code=shedule_plan["code"], recruitment_year = shedule_plan["recruitment_year"],
                                    form = shedule_plan["education_form"],period=shedule_plan["period"],
                                    oop = OOP(code=oop_detail["code"],direction=oop_detail["direction"],
                                            eduction_profile=oop_detail["eduction_profile"],
                                            education_level=oop_detail["education_level"]),
                                    disciplines=[])
    return {
            "name":group["name"],
            "year_of_recruitment":group["year_of_recruitment"],
            "available_places":group["available_places"],
            "potential_places":group["potential_places"],
            "course":group["course"], "end_year":group["end_year"],
            "shedule_plan":shedule_plan_detail}

odd_responses = {
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "404",
                        "value": {"code": 404, "message": "Not Found"}
                    },
                }
            }
        }
    },
}

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

