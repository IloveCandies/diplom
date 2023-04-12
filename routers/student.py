from fastapi import APIRouter
from mock_data import *
from shemas import *

student_router = APIRouter()

@student_router.post("/student/add/", summary="Добавить новый университета")
async def add_student() -> Student: 
    return Student

@student_router.get("/student/", summary="Получить данные университета")
async def get_student(id) -> Student: 
    return Student

@student_router.patch("/student/path/", summary="Обновить данные университета")
async def path_student(id) -> Student: 
    return Student
   
@student_router.delete("/student/delete/", summary="Удалить университет")
async def delete_student(id) -> Student: 
    return Student

@student_router.get("/students/", summary="Получить данные всех университет")
async def get_students() -> List[Student]: 
    return List[Student]