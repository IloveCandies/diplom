from fastapi import APIRouter, Depends, Response,  Security, Request
from shemas import *
from asyncpg import exceptions
from db.init import database
from db.models import city_table, region_table
from fastapi.responses import JSONResponse
from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError

region_router = APIRouter(responses={400: {"model": Message}, 401: {"model": Message},404: {"model": Message}, 422: {"model": Message}})

@region_router.post("/region/add/", summary="Добавить новый регион")
async def add_region(item:Region) -> bool: 
    query = region_table.insert().values(code = item.code, name = item.name)
    try:
        await database.execute(query=query)
        return True
    except IntegrityError:
        return JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Регион с таким кодом или названием уже существует"}})
    except UniqueViolationError:
        return  JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Регион с таким кодом или названием уже существует"}})



@region_router.get("/region/", summary="Получить данные региона")
async def get_region(code:int):
    query = region_table.select().where(region_table.c.code == code)
    current_region = await database.fetch_one(query)
    print(current_region)            
    if current_region == None:
        return JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Региона с таким кодом не существует"}})                     
    return Region(code = current_region.code,name = current_region.name)

@region_router.get("/regions/", summary="Получить данные всех регионов")
async def get_regions() -> List[Region]:
    query = region_table.select() 
    current_regions = []
    regions = await database.fetch_all(query)
    for region in regions:
        current_regions.append(Region(code = region.code,name = region.name))
    return current_regions

@region_router.patch("/region/path/", summary="Обновить данные региона")
async def path_region(code:int, item:Region) -> Region: 
    query = region_table.update().values(
        code = item.code, name = item.name
    ).where(region_table.c.code == code)
    await database.execute(query)
    return await get_region(item.code)
   


@region_router.delete("/region/delete/", summary="Удалить регион", deprecated=True)
async def delete_region(code:int) -> Region: 
    return Region


