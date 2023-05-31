from fastapi import APIRouter
from shemas import *

region_router = APIRouter()

@region_router.post("/region/add/", summary="Добавить новый университета")
async def add_region() -> University: 
    return University

@region_router.post("/region/add/city", summary="Прикрепить город к региону")
async def add_region() -> University: 
    return University

@region_router.get("/region/", summary="Получить данные университета")
async def get_region(id) -> University: 
    return University

@region_router.patch("/region/path/", summary="Обновить данные университета")
async def path_region(id) -> University: 
    return University
   
@region_router.delete("/region/delete/", summary="Удалить университет")
async def delete_region(id) -> University: 
    return University

@region_router.get("/universities/", summary="Получить данные всех университет")
async def get_regions() -> List[University]: 
    return List[University]

