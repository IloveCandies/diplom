from fastapi import APIRouter
from shemas import *

user_router = APIRouter()

@user_router.post("/api/v1/add_to_favorite_list/")
async def add_to_favorite_list(user_id:str, group_id:int) -> Student:
    user =  [x for x in Students if x.id == user_id ][0]
    group = [x for x in Groups if x.id == group_id ][0]
    user.favorite_list.groups.append(group)
    return user

@user_router.get("/api/v1/get_favorite_list/")
async def get_list(user_id:str) -> FavoriteList:
    user =  [x for x in Students if x.id ==user_id ][0]
    return user.favorite_list

    