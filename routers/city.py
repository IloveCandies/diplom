from fastapi import APIRouter, Depends, Response,  Security, Request
from shemas import *
from asyncpg import exceptions
from db.init import database
from db.models import city_table, region_table
from fastapi.responses import JSONResponse
from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError
from .region import get_region
city_router = APIRouter(responses={400: {"model": Message}, 401: {"model": Message},404: {"model": Message}, 422: {"model": Message}})


@city_router.get("/city/", summary="Получить данные города")
async def get_city(city_name) -> University: 
    query = city_table.select().where(city_table.c.city_name == city_name)
    current_city = await database.fetch_one(query)
    if current_city == None:
        return JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Города с таким названием не существует в базе данных"}})                     
    return City(region_code = current_city.region_code,city_name = current_city.city_name)

@city_router.get("/cities/", summary="Получить данные всех университет")
async def get_cities() -> List[University]: 
    query = city_table.select() 
    current_sities = []
    cities = await database.fetch_all(query)
    for city in cities:
        current_sities.append(City(region_code = city.region_code,city_name = city.city_name))
    return List[University]

@city_router.post("/city/add/", summary="Добавить новый город")
async def add_city(item:City) -> bool: 
    query = region_table.select().where(region_table.c.code == item.region_code)
    region = await  database.fetch_one(query)
    print(region)
    if region == None:
        return JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Региона с таким кодом  не существует в базе"}})
    query = city_table.insert().values(region_code = item.region_code, city_name = item.city_name)
    try:
        await database.execute(query=query)
        return True
    except IntegrityError:
        return JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Город с таким названием уже существует"}})
    except UniqueViolationError:
        return  JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Город с таким названием уже существует"}})
        

@city_router.post("/city/add/region", summary="Прикрепить город к региону")
async def add_region_to_city(city_name :str, region_code:int) -> Region: 
    query = city_table.update.values(region_code = region_code).where(city_table.c.region_code == region_code)
    await database.execute(query)
    return await get_city
    

@city_router.patch("/city/path/", summary="Обновить данные университета",deprecated=True)
async def path_city(id) -> University: 
    return University
   
@city_router.delete("/city/delete/", summary="Удалить университет",deprecated=True)
async def delete_city(id) -> University: 
    return University

