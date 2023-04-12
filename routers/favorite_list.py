from fastapi import APIRouter
from mock_data import *
from shemas import *

favorite_list_router = APIRouter()

@favorite_list_router.post("/favorites/add/", summary="Добавить новый университета")
async def add_group_to_favorites() -> Student: 
    return Student
   
@favorite_list_router.delete("/favorites/remove/", summary="Удалить университет")
async def remove_group_to_favorites(id) -> Student: 
    return Student
