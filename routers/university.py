from fastapi import APIRouter
from shemas import *

university_router = APIRouter()

@university_router.post("/university/add/", summary="Добавить новый университета", deprecated=True)
async def add_university() -> University: 
    return University

@university_router.post("/university/add/city", summary="Добавить новый университета", deprecated=True)
async def add_university() -> University: 
    return University

@university_router.post("/university/remove/city", summary="Добавить новый университета", deprecated=True)
async def add_university() -> University: 
    return University

@university_router.post("/university/add/group", summary="Добавить новый университета", deprecated=True)
async def add_university() -> University: 
    return University

@university_router.post("/university/remove/group", summary="Добавить новый университета", deprecated=True)
async def add_university() -> University: 
    return University

@university_router.post("/university/add/staff", summary="Добавить новый университета", deprecated=True)
async def add_university() -> University: 
    return University

@university_router.post("/university/remove/staff", summary="Добавить новый университета", deprecated=True)
async def add_university() -> University: 
    return University

@university_router.get("/university/", summary="Получить данные университета", deprecated=True)
async def get_university(id) -> University: 
    return University

@university_router.patch("/university/path/", summary="Обновить данные университета", deprecated=True)
async def path_university(id) -> University: 
    return University
   
@university_router.delete("/university/delete/", summary="Удалить университет", deprecated=True)
async def delete_university(id) -> University: 
    return University

@university_router.get("/universities/", summary="Получить данные всех университет", deprecated=True)
async def get_universitys() -> List[University]: 
    return List[University]

