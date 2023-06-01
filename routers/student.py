from fastapi import APIRouter, Depends, Response,  Security, Request
from shemas import *
from asyncpg import exceptions
from db.init import database
from db.models import favorites_item_table, favorites_table, group_table, student_table
from .groups import get_group
from fastapi.responses import JSONResponse

student_router = APIRouter(responses={400: {"model": Message}, 401: {"model": Message},404: {"model": Message}, 422: {"model": Message}})


async def update_student_by_id(id) -> bool: 
    return Student



@student_router.get("/student/{id}", summary="Получить данные студента")
async def get_student_by_id(id:int) -> Student: 
    query = student_table.select().where(student_table.c.id == id)
    student = await database.fetch_one(query)
    if student == None:
        return JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Пользователя с таким именем не существует "}})

    return Student(first_name=student["first_name"],middle_name=student["middle_name"],
                    last_name=student["last_name"],phone=student["phone"], city = None)


@student_router.get("/student/", summary="Получить данные студента через email")
async def get_student_by_email(email:str) -> Student:
    query = student_table.select().where(student_table.c.email == email)
    student = await database.fetch_one(query)
    if student == None:
        return JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Пользователя с таким именем не существует "}})

    return Student(first_name=student["first_name"],middle_name=student["middle_name"],
                    last_name=student["last_name"],phone=student["phone"], city = None) 

@student_router.patch("/student/{id}/path/", summary="Обновить данные студента из админки")
async def path_student(id:int, new_student_data: StudentData) -> Student: 
    query = student_table.update().values( first_name = new_student_data.last_name, 
                                         middle_name = new_student_data.middle_name ,
                                         last_name = new_student_data.last_name ).where(student_table.c.id == id)
    await database.execute(query)
    return await get_student_by_id(id)


@student_router.patch("/student/path/", summary="Обновить данные в настройках (через куки)")
async def path_student(new_student_data: StudentData, request: Request, ) -> Student: 
    user_id = int(request.cookies.get("user_id"))
    query = student_table.update().values( first_name = new_student_data.last_name, 
                                         middle_name = new_student_data.middle_name ,
                                         last_name = new_student_data.last_name ).where(student_table.c.id == user_id)
    await database.execute(query)
    return await get_student_by_id(user_id)


@student_router.get("/students/", summary="Получить данные всех студентов")
async def get_students() -> List[Student]: 
    query = student_table.select()
    return await database.fetch_all(query)

   
@student_router.delete("/student/delete/", summary="Удалить студента", deprecated=True)
async def delete_student(id) -> Student: 
    return Student
