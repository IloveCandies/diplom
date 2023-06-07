from fastapi import APIRouter, Depends, Response,  Security, Request
from shemas import *
from db.models import staff_table, student_table
from fastapi.responses import JSONResponse
from db.init import database
from middleware import hashing
from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError
from middleware.jwt import *
from db.models import *

from .university import get_university

university_staff_router =  APIRouter(responses={400: {"model": Message}, 401: {"model": Message},404: {"model": Message}, 422: {"model": Message}})


@university_staff_router.post("/university/staff/create", summary="Получить данные об  сотруднике")
async def create_staff(response: Response,request: Request, staff_data:UniversityStaffData ) -> bool: 
    values = { "first_name":staff_data.first_name,"middle_name":staff_data.middle_name, 
                "last_name":staff_data.last_name,
                "phone":staff_data.phone, "email":staff_data.email}

    password, salt = await hashing.encode_password(staff_data.password)
    values["password"],values["salt"] = password, salt 
    token = access_security.create_access_token(subject=values)
    values["api_token"] = token

    query = """INSERT INTO "UniversityStaff" (first_name, last_name, middle_name,
    phone, email, password, salt, api_token, university ) 
    SELECT :first_name,:middle_name,:last_name, :phone, :email, :password, :salt, :api_token, :university
    RETURNING  id"""
    
    _university_query = university_table.select().where(university_table.c.name ==staff_data.university) 
    _university = await database.fetch_one(_university_query)
    if _university == None:
        return JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Университета с таким названием не существует в базе данных"}}) 
    values["university"] = _university.name
    try:
        await database.execute(query=query, values=values)
        return True
    except IntegrityError:
        return JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Пользователь с таким телефоном или почтой уже существует"}})
    except UniqueViolationError:
        return  JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Пользователь с таким телефоном или почтой уже существует"}})


@university_staff_router.get("/university/staff/", summary="Получить данные об  сотруднике")
async def get_staff(staff_email:str) -> UniversityStaffData: 
    query = staff_table.select().where(staff_table.c.email == staff_email)

    staff_data = await database.fetch_one(query)
    if staff_data == None:
        return JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Пользовательс такой почтой не существует"}})
    return UniversityStaffData(first_name =staff_data.first_name,middle_name = staff_data.middle_name, 
                last_name=staff_data.last_name, phone =staff_data.phone, email=staff_data.email, university=staff_data.university)
        

@university_staff_router.get("/university/staff/{staff_id}", summary="Получить данные об  сотруднике")
async def get_staff(staff_id:int) -> UniversityStaffData: 
    query = staff_table.select().where(staff_table.c.id == staff_id)
    staff_data = await database.fetch_one(query)
    if staff_data == None:
        return JSONResponse(status_code=422, content = {"detail":
                            {"datetime":datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                            "msg": "Пользователь с таким id не существует"}})
    return UniversityStaffData(first_name =staff_data.first_name,middle_name = staff_data.middle_name, 
                last_name=staff_data.last_name, phone =staff_data.phone, email=staff_data.email, university=staff_data.university)


@university_staff_router.get("/university/staff/all/", summary="Получить данные об  сотруднике")
async def get_staff() -> List[UniversityStaffData]: 
    query = staff_table.select()
    staff_data = await database.fetch_all(query)
    staff_list = []
    for staff in staff_data:
        staff_list.append( UniversityStaffData(first_name =staff.first_name,middle_name = staff.middle_name, 
                last_name=staff.last_name, phone =staff.phone, email=staff.email, university=staff.university))
    return staff_list


@university_staff_router.patch("/university/staff/path/", summary="Обновить данные  сотрудникае", deprecated=True)
async def path_student_education(staff_id) -> UniversityStaff: 
    return UniversityStaff
   
@university_staff_router.delete("/university/staff/", summary="Удалить сотрудника", deprecated=True)
async def delete_student_education(staff_id) -> UniversityStaff: 
    return UniversityStaff
