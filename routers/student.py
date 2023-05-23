from fastapi import APIRouter
from shemas import *

student_router = APIRouter()

@student_router.post("/student/add/", summary="Добавить нового студента")
async def add_student() -> Student: 
    return Student

@student_router.get("/student/", summary="Получить данные студента")
async def get_student(id) -> Student: 
    return Student

@student_router.patch("/student/path/", summary="Обновить данные студента")
async def path_student(id) -> Student: 
    return Student
   
@student_router.delete("/student/delete/", summary="Удалить студента")
async def delete_student(id) -> Student: 
    return Student

@student_router.get("/students/", summary="Получить данные всех студентов")
async def get_students() -> List[Student]: 
    return List[Student]