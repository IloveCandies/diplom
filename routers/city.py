from fastapi import APIRouter
from shemas import *

city_router = APIRouter()

@city_router.post("/city/add/", summary="Добавить новый университета")
async def add_city() -> University: 
    return University

@city_router.post("/city/add/region", summary="Прикрепить город к региону")
async def add_region_to_city() -> Region: 
    return Region
    
@city_router.get("/city/", summary="Получить данные университета")
async def get_city(id) -> University: 
    return University

@city_router.patch("/city/path/", summary="Обновить данные университета")
async def path_city(id) -> University: 
    return University
   
@city_router.delete("/city/delete/", summary="Удалить университет")
async def delete_city(id) -> University: 
    return University

@city_router.get("/universities/", summary="Получить данные всех университет")
async def get_citys() -> List[University]: 
    return List[University]
