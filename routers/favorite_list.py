from fastapi import APIRouter, Depends, Response,  Security, Request
from shemas import *
from asyncpg import exceptions
from db.init import database
from db.models import favorites_item_table, favorites_table, group_table, student_table
from .groups import get_group,get_group_by_id
from fastapi.responses import JSONResponse

favorite_list_router =  APIRouter(responses={400: {"model": Message}, 401: {"model": Message},404: {"model": Message}, 422: {"model": Message}})

async def get_list_id(user_id):
    query =  favorites_table.select().where(favorites_table.c.student == user_id)
    favorite_list = await database.fetch_one(query)
    return favorite_list["id"]

async def get_all_items_details(user_id) -> FavoriteList:
    user_favorite_list = FavoriteList(groups=[])
    user_favorite_list_id = await get_list_id(user_id)
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

@favorite_list_router.post("/favorites/add/", summary="Добавить группу в список избранного")
async def add_group_to_favorites(group_name:str, response: Response, request: Request, 
                                 message:str = "Вот мой сопроводительный текст: Хочу на бюджет потому что я крутой") -> bool:
    
    user_id = int(request.cookies.get("user_id"))
    
    query = favorites_table.insert().values(student = user_id)
    
    group_query = group_table.select().where(group_table.c.name == group_name)
    group = await database.fetch_one(group_query)
    group_id = group["id"]
    
    if group_id == None:
        return JSONResponse(status_code=400, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Группа с таким именем не существует "}})
    
    item_query  = """INSERT INTO "FavoriteItem" (favorite_list_id, group_id, message)
                        SELECT :favorite_list_id, :group_id, :message
                        WHERE
                        NOT EXISTS (
                        SELECT CAST(:group_id AS INTEGER ) FROM "FavoriteItem" WHERE group_id = :group_id)
                        RETURNING  id"""
    try:
        favorite_list_id = await database.execute(query)
        
        await database.execute(group_query)
        await database.execute(item_query,values={"favorite_list_id":favorite_list_id,"group_id":group_id,"message":message,})
        return True
    
    except (exceptions.UniqueViolationError):
        query = favorites_table.select().where(favorites_table.c.student == user_id)
        favorite_list = await database.fetch_one(query)
    
        await database.execute(group_query)
        favorite_list_id = favorite_list["id"]
        await database.execute(item_query,values={"favorite_list_id":favorite_list_id,"group_id":group_id,"message":message,})
        
        query = favorites_table.select().where(favorites_item_table.c.id == favorite_list_id)
        favorite_list_item = await database.execute(query)
        favorite_list_item_id = favorite_list_item


        print(favorite_list_item_id,favorite_list_id,group_id,message)
        return True
    

@favorite_list_router.get("/favorites/")
async def get_favorites(request: Request) -> FavoriteList: 
    user_id = int(request.cookies.get("user_id"))
    print(user_id)
    user_favorite_list = FavoriteList(groups=[])
    user_favorite_list_id = await get_list_id(user_id)
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
   
@favorite_list_router.delete("/favorites/remove/", summary="Удалить из списка избранного  НЕ ДОДЕЛАННО")
async def remove_group_from_list(group_name:str, request: Request):
    user_id = int(request.cookies.get("user_id"))
    favorite_list_id = await get_list(user_id)
    
    query = group_table.select().where(group_table.c.name == group_name)
    group_id = await database.execute(query)
    
    query = favorites_item_table.delete().where((favorites_item_table.c.group_id == group_id) 
                                                and ( favorites_item_table.c.favorite_list_id  == favorite_list_id))
    try:
        await database.execute(query)
        return await get_all_items_details(user_id)
    except:
            raise Exception("Непредвиденная ошибка")