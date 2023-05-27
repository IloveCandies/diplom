from fastapi import APIRouter, Depends, Response,  Security, Request
from shemas import *
from db.models import staff_table, student_table
from fastapi.responses import JSONResponse
from db.init import database
from middleware import hashing
from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError
from middleware.jwt import *



auth_router = APIRouter (
    responses={404: {"description": "Not found"}})


@auth_router.post("/sign_up/staff/", summary="")
async def auth(response: Response,request: Request, login_data:LoginData ): 
    values = { "first_name":login_data.first_name,"middle_name":login_data.middle_name, 
                "last_name":login_data.last_name,
                "phone":login_data.phone, "email":login_data.email 
            }

    password, salt = await hashing.encode_password(login_data.password)
    values["password"],values["salt"] = password, salt 
    token = access_security.create_access_token(subject=values)
    values["api_token"] = token

    query = """INSERT INTO "UniversityStaff" (first_name, last_name, middle_name,
    phone, email, password, salt, api_token) 
    SELECT :first_name,:middle_name,:last_name, :phone, :email, :password, :salt, :api_token
    RETURNING  id"""

    try:
        await database.execute(query=query, values=values)
        return True
    except IntegrityError:
        return {"message": "Пользователь с таким телефоном или почтой уже существует"}
    except UniqueViolationError:
        return {"message": "Пользователь с таким телефоном или почтой уже существует"}
    return {"message": "Пользователь с таким телефоном или почтой уже существует"}

    

@auth_router.post("/sign_up/student/", summary="")
async def auth(response: Response,request: Request, login_data:LoginData ): 
    values = { "first_name":login_data.first_name,"middle_name":login_data.middle_name, 
    "last_name":login_data.last_name,"phone":login_data.phone, "email":login_data.email }

    password, salt = await hashing.encode_password(login_data.password)
    values["password"],values["salt"] = password, salt 

    query = """INSERT INTO "Student" (first_name, last_name, middle_name,
    phone, email, password, salt) 
    SELECT :first_name,:middle_name,:last_name, :phone, :email, :password, :salt
    RETURNING  id"""
    await database.execute(query=query, values=values)
    
    try:
        await database.execute(query=query, values=values)
        return True
    except IntegrityError:
        return {"message": "Пользователь с таким телефоном или почтой уже существует"}
    except UniqueViolationError:
        return {"message": "Пользователь с таким телефоном или почтой уже существует"}


#JSONResponse(status_code=404, content = {"description": "Not found","request_date":datetime.datetime.now().timestamp()
@auth_router.post("/sign_in/staff/", summary="")
async def sign_in(email:str, password:str)->UniversityStaffRecord: 
    query = staff_table.select().where(staff_table.c.email == email)
    staff = await database.fetch_one(query)
    if await hashing.check_password(password,staff["password"],staff["salt"]) == True:
        return staff
    else:
        return staff["password"]

#JSONResponse(status_code=404, content = {"description": "Not found","request_date":datetime.datetime.now().timestamp()
@auth_router.post("/sign_in/student/", summary="")
async def sign_in(email:str, password:str, response: Response)->Student: 
    query = student_table.select().where(student_table.c.email == email)
    student = await database.fetch_one(query)
    if await hashing.check_password(password,student["password"],student["salt"]) == True:
        response.set_cookie(key="user_id", value = student["id"])    
        return student
    else:
        return student["password"]

@auth_router.post("/logout/", summary="")
async def logout() -> UniversityStaff: 
    return UniversityStaff

async def refresh_token (token:JwtAuthorizationCredentials = Security(access_security)) -> UniversityStaffRecord:
    query = staff_table.select().where(staff_table.c.api_token == token)
    staff = await database.fetch_one(query)
    return staff   


@auth_router.get("/refresh/token", summary="")
async def whoami(): 
    token = access_security.create_access_token(subject={})
    ref_token = access_security.create_refresh_token(subject={})
    return token, ref_token

@auth_router.get("/whoami/", summary="")
async def whoami(token:JwtAuthorizationCredentials = Security(access_security)): 
    return token
