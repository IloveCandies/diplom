from fastapi import APIRouter
from mock_data import *
from shemas import *

groups_router = APIRouter()

@groups_router.post("/group/add/", summary="Добавить новую группу")
async def add_group() -> Group: 
    return Group

@groups_router.get("/group/", summary="Получить данные конкретной группы по id")
async def get_group(id) -> Group: 
    return Group

@groups_router.patch("/group/path/", summary="Обновить данные группы, взятой по id")
async def get_group(id) -> Group: 
    return Group
   
@groups_router.delete("/group/delete/", summary="Удалить групу, взятую по id")
async def get_group(id) -> Group: 
    return Group

@groups_router.get("/groups/", summary="Получить данные всех групп")
async def get_groups() -> List[Group]: 
    return List[Group]

@groups_router.delete("/groups/delete/", summary="Удалить группу из списка")
async def get_groups(id) -> List[Group]: 
    return List[Group]