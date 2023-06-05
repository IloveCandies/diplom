from fastapi import APIRouter, Depends, Response,  Security, Request
from shemas import *
from asyncpg import exceptions
from db.init import database
from db.models import favorites_item_table, favorites_table, group_table, student_table
from .groups import get_group,get_group_by_id
from fastapi.responses import JSONResponse
from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError

favorite_list_router =  APIRouter(responses={400: {"model": Message}, 401: {"model": Message},404: {"model": Message}, 422: {"model": Message}})

async def get_list_id(student_id):
    query =  favorites_table.select().where(favorites_table.c.student == student_id)
    favorite_list = await database.fetch_one(query)
    if favorite_list == None:
        insert_query =  favorites_table.insert().values(student = student_id)
        await database.execute(insert_query)
        favorite_list = await database.fetch_one(query)
    print("id",favorite_list["id"])
    return favorite_list["id"]

async def get_all_items_details(student_id) -> FavoriteList:
    user_favorite_list = FavoriteList(groups=[])
    user_favorite_list_id = await get_list_id(student_id)
    query =  favorites_item_table.select().where(favorites_item_table.c.favorite_list_id == user_favorite_list_id)
    answ = await database.fetch_all(query)
    for item in answ:
        group = await get_group_by_id(item["group_id"])
        user_favorite_list.groups.append(StudentFavoriteListItem(group = group, message = item["message"]))
    print(user_favorite_list)
    return  user_favorite_list





async def update_comment(favorite_list_item_id,favorite_list_id,group_id,message):
    update_comment_query =  favorites_item_table.update().values(
        message = message).where((favorites_item_table.c.id == favorite_list_item_id) 
        and(favorites_item_table.c.favorite_list_id == favorite_list_id)
        and(favorites_item_table.c.group_id == group_id))
    await database.execute(update_comment_query)

@favorite_list_router.post("/favorites/add/", summary="Добавить группу в список избранного",description="id студента берется из cookies")
async def add_group_to_favorites(group_name:str, response: Response, request: Request, 
                                 message:str = "Вот мой сопроводительный текст: Хочу на бюджет потому что я крутой"):
    student_id = int(request.cookies.get("student_id"))
    group_query = group_table.select().where(group_table.c.name == group_name)
    group = await database.fetch_one(group_query)
    _favorite_list_id = await get_list_id(student_id)
    
    if group == None:
        return JSONResponse(status_code=400, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Группа с таким именем не существует "}})
    _group_id = group["id"]

    favorite_item_query = favorites_item_table.insert().values(favorite_list_id = _favorite_list_id, group_id = _group_id,message = message)
    await database.execute(group_query)
    await database.execute(favorite_item_query)
    return True


@favorite_list_router.post("/student/{student_id}/favorites/add/", summary="Добавить группу в список избранного")
async def add_group_to_favorites(group_name:str, student_id:int, response: Response, request: Request, 
                                 message:str = "Вот мой сопроводительный текст: Хочу на бюджет потому что я крутой"):
    group_query = group_table.select().where(group_table.c.name == group_name)
    group = await database.fetch_one(group_query)
    _favorite_list_id = await get_list_id(student_id)

    if group == None:
        return JSONResponse(status_code=400, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Группа с таким именем не существует "}})
    _group_id = group["id"]
    favorite_item_query = favorites_item_table.insert().values(favorite_list_id = _favorite_list_id, group_id = _group_id,message = message)
    await database.execute(group_query)
    await database.execute(favorite_item_query)
    return True
    
@favorite_list_router.get("/favorites/",summary="Показать список избранного студента",description="id студента берется из cookies")
async def get_favorites(request: Request) -> FavoriteList: 
    student_id = int(request.cookies.get("student_id"))
    print(student_id)
    user_favorite_list = FavoriteList(groups=[])
    user_favorite_list_id = await get_list_id(student_id)
    print(user_favorite_list_id)
    query =  favorites_item_table.select().where(favorites_item_table.c.favorite_list_id == user_favorite_list_id)
    answ = await database.fetch_all(query)
    print(answ)
    for item in answ:
        print(item)
        group = await get_group_by_id(item["group_id"])
        print(group)
        user_favorite_list.groups.append(StudentFavoriteListItem(group = group, message = item["message"]))
    print(user_favorite_list)
    print(type(user_favorite_list))
    return  user_favorite_list.dict()
   

@favorite_list_router.get("/student/{student_id}/favorites/",summary="Показать список избранного студента",description="id студента берется из cookies")
async def get_favorites(student_id:int, request: Request) -> FavoriteList: 
    print(student_id)
    user_favorite_list = FavoriteList(groups=[])
    user_favorite_list_id = await get_list_id(student_id)
    print(user_favorite_list_id)
    query =  favorites_item_table.select().where(favorites_item_table.c.favorite_list_id == user_favorite_list_id)
    answ = await database.fetch_all(query)
    print(answ)
    for item in answ:
        print(item)
        group = await get_group_by_id(item["group_id"])
        print(group)
        user_favorite_list.groups.append(StudentFavoriteListItem(group = group, message = item["message"]))
    print(user_favorite_list)
    print(type(user_favorite_list))
    return  user_favorite_list.dict()
   

@favorite_list_router.post("/favorites/remove/", summary="Удалить из списка избранного  НЕ ДОДЕЛАННО")
async def remove_group_from_list(group_name:str,request: Request):
    student_id = int(request.cookies.get("student_id"))
    favorite_list_id = await get_list_id(student_id)
    
    query = group_table.select().where(group_table.c.name == group_name)
    group_id = await database.execute(query)
    
    query = favorites_item_table.delete().where((favorites_item_table.c.group_id == group_id) 
                                                and ( favorites_item_table.c.favorite_list_id  == favorite_list_id))
    try:
        await database.execute(query)
        return await get_all_items_details(student_id)
    except:
            raise Exception("Непредвиденная ошибка")

favorite_list_router.post("/student/{student_id}/favorites/remove/", summary="Удалить из списка избранного  НЕ ДОДЕЛАННО")
async def remove_group_from_list(group_name:str, student_id:int ,request: Request):
    favorite_list_id = await get_list_id(student_id)
    
    query = group_table.select().where(group_table.c.name == group_name)
    group_id = await database.execute(query)
    
    query = favorites_item_table.delete().where((favorites_item_table.c.group_id == group_id) 
                                                and ( favorites_item_table.c.favorite_list_id  == favorite_list_id))
    try:
        await database.execute(query)
        return await get_all_items_details(student_id)
    except:
            raise Exception("Непредвиденная ошибка")