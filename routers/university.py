from fastapi import APIRouter
from shemas import *

university_router = APIRouter()

@university_router.post("/api/v1/university/add/", summary="Добавить новый университета")
async def add_university() -> University: 
    return University

@university_router.get("/api/v1/university/", summary="Получить данные университета")
async def get_university(id) -> University: 
    return University

@university_router.patch("/api/v1/university/path/", summary="Обновить данные университета")
async def path_university(id) -> University: 
    return University
   
@university_router.delete("/api/v1/university/delete/", summary="Удалить университет")
async def delete_university(id) -> University: 
    return University

@university_router.get("/api/v1/universities/", summary="Получить данные всех университет")
async def get_universitys() -> List[University]: 
    return List[University]

