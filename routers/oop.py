
from fastapi import APIRouter
from asyncpg import exceptions
from shemas import *
from db.models import oop_table
from db.init import database
from fastapi.responses import JSONResponse
oop_router = APIRouter( responses={404: {"description": "Not found"}})

@oop_router.get("/api/v1/oop/")
async def get_oop(id:int) -> OOPTableRecord:
    query = oop_table.select().where(oop_table.c.id == id)
    print(query)
    return await database.fetch_one(query)

@oop_router.get("/api/v1/oop/list/")
async def get_list_oop() -> List[OOPTableRecord]:
    query = oop_table.select()
    print(query)
    return await database.fetch_all(query)

@oop_router.post("/api/v1/oop/create/")
async def create(item: OOP) -> OOP:
    if item.code.isdigit() or item.direction.isdigit() == True:
        print(item.code.isdigit())
        return JSONResponse(status_code=402, content = {"description": "Value Type Error check the shema    "})  
    else:
        try:
            query = oop_table.insert().values (
            code=item.code, direction=item.direction,
            eduction_profile = item.eduction_profile,
            education_level = item.education_level )
            print(query)        
            await database.execute(query)

        except (ValueError):
            raise Exception("Ошибка в значении переменной, проверьте данные со схемой")
        except (exceptions.UniqueViolationError):
           return JSONResponse(status_code=422, content = {"description": "Обьект с таким кодом уже существует"})
        return item

@oop_router.patch("/api/v1/oop/path/")
async def update(item: OOPTableRecord) -> OOP:
    if item.code.isdigit() or item.direction.isdigit() == True:
        print(item.code.isdigit())
        return JSONResponse(status_code=402, content = {"description": "Value Type Error check the shema    "})  
    else:
        try:
            query = oop_table.update().values(
                code=item.code, direction=item.direction,
                eduction_profile = item.eduction_profile,
                education_level = item.education_level,
                ).where(oop_table.c.id == item.id)
            await database.execute(query)
        except (ValueError):
            raise Exception("Ошибка в значении переменной, проверьте данные со схемой")
        except (IndexError):
            raise Exception("Обьект с теким индексом уже существует")
        return item

@oop_router.delete("/api/v1/oop/delete/")
async def delete_oop(id:int):
    try:
        query = oop_table.delete().where(oop_table.c.id ==id)
        await database.execute(query)
        return {'delete':True}
    except:
            raise Exception("Непредвиденная ошибка")
