from fastapi import APIRouter
from mock_data import *
from shemas import *

university_router = APIRouter()

@university_router.post("/university/add/", summary="Добавить новый университета")
async def add_university() -> University: 
    return University

@university_router.get("/university/", summary="Получить данные университета")
async def get_university(id) -> University: 
    return University

@university_router.patch("/university/path/", summary="Обновить данные университета")
async def path_university(id) -> University: 
    return University
   
@university_router.delete("/university/delete/", summary="Удалить университет")
async def delete_university(id) -> University: 
    return University

@university_router.get("/universities/", summary="Получить данные всех университет")
async def get_universitys() -> List[University]: 
    return List[University]

