from fastapi import APIRouter, Depends, Response,  Security, Request
from shemas import *
from asyncpg import exceptions
from db.init import database
from db.models import city_table, region_table
from fastapi.responses import JSONResponse
from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError
from db.models import *
from .city import get_city
university_router = APIRouter(responses={400: {"model": Message}, 401: {"model": Message},404: {"model": Message}, 422: {"model": Message}})


@university_router.post("/university/add/", summary="Добавить университет")
async def add_university(item:University) -> bool:
   
    query = city_table.select().where(city_table.c.city_name  == item.сity)
    city = await database.fetch_one(query)
    if city == None:
        return JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Города с таким названием не существует в базе данных"}}) 
    query = university_table.insert().values(name = item.name, 
                city = city.city_name, description = item.description) 

    try:
        await database.execute(query=query)
        return True
    except IntegrityError:
        return JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Университет с таким названием уже существует"}})
    except UniqueViolationError:
        return  JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Университет с таким названием уже существует"}})
    return  True



@university_router.get("/university/", summary="Получить данные университета")
async def get_university(university_name:str) -> University:
    query = university_table.select().where(university_table.c.name == university_name) 
    university = await database.fetch_one(query)
    print(university.city) 
    if university == None:
        return JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Университета с таким названием не существует в базе данных"}}) 
    return University(name=university.name, сity = university.city, 
                        description=university.description)

@university_router.patch("/university/path/", summary="Обновить данные университета", deprecated=True)
async def path_university(id) -> University: 
    return University
   
@university_router.delete("/university/delete/", summary="Удалить университет")
async def delete_university(university_name:str) -> University: 
    query = university_table.delete().where(university_table.c.name == university_name) 
    await database.fetch_one(query)
    return University

@university_router.get("/universities/", summary="Получить данные всех университет")
async def get_universitys() -> List[University]:
    universities =[]
    query = university_table.select()
    current_universities =  await database.execute(query)
    for university in current_universities:
        universities.append(University(name=university.name,city =university.city, description= university.description))

    return List[University]

