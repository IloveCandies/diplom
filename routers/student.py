
from fastapi import APIRouter, Depends, Response,  Security, Request
from shemas import *
from asyncpg import exceptions
from db.init import database
from db.models import favorites_item_table, favorites_table, group_table, student_table
from .groups import get_group,get_group_by_id

student_router = APIRouter(responses={404: {"model": Message},400: {"model": Message}, 401: {"model": Message}} )


async def update_student_by_id(id) -> bool: 
    return Student

async def get_student_by_id(id:int) -> Student: 
    query = student_table.select().where(student_table.c.id == id)
    student = await database.fetch_one(query)
    return Student(first_name=student["first_name"],middle_name=student["middle_name"],
                    last_name=student["last_name"],phone=student["phone"], city = None)

@student_router.post("/api/v1/student/add/", summary="Добавить нового студента")
async def add_student() -> Student: 
    return Student

@student_router.get("/api/v1/student/", summary="Получить данные студента")
async def get_student(name:str) -> Student:
    query = student_table.select().where(student_table.c.id == id)
    student = await database.fetch_one(query)
    return Student(first_name=student["first_name"],middle_name=student["middle_name"],
                    last_name=student["last_name"],phone=student["phone"], city = None) 
    
@student_router.patch("/api/v1/student/path/", summary="Обновить данные студента")
async def path_student(new_student_data: StudentData, request: Request, ) -> Student: 
    user_id = int(request.cookies.get("user_id"))
    query = student_table.update().values( first_name = new_student_data.last_name, 
                                         middle_name = new_student_data.middle_name ,
                                         last_name = new_student_data.last_name ).where(student_table.c.id == user_id)
    await database.execute(query)
    
    return await get_student_by_id(user_id)

@student_router.post("/api/v1/student/add/education/", summary="Обновить данные студента")
async def path_student(user) -> Student: 
    return Student


   
@student_router.delete("/api/v1/student/delete/", summary="Удалить студента")
async def delete_student(id) -> Student: 
    return Student

@student_router.get("/api/v1/students/", summary="Получить данные всех студентов")
async def get_students() -> List[Student]: 
    return List[Student]