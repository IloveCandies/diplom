from fastapi import APIRouter
from shemas import *

student_router = APIRouter()

@student_router.post("/api/v1/student/add/", summary="Добавить нового студента")
async def add_student() -> Student: 
    return Student

@student_router.get("/api/v1/student/", summary="Получить данные студента")
async def get_student(id) -> Student: 
    return Student

@student_router.patch("/api/v1/student/path/", summary="Обновить данные студента")
async def path_student(id) -> Student: 
    return Student
   
@student_router.delete("/api/v1/student/delete/", summary="Удалить студента")
async def delete_student(id) -> Student: 
    return Student

@student_router.get("/api/v1/students/", summary="Получить данные всех студентов")
async def get_students() -> List[Student]: 
    return List[Student]