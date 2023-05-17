from fastapi import APIRouter, Depends, Response,  Security, Request
from shemas import *
from db.models import staff_table
from fastapi.responses import JSONResponse
from db.init import database
from middleware import hashing
from middleware.jwt import *



auth_router = APIRouter (
    responses={404: {"description": "Not found"}})


@auth_router.post("/sign_up/staff/", summary="")
async def auth(response: Response,request: Request, login_data:LoginData ): 
    values = { "first_name":login_data.first_name,"middle_name":login_data.middle_name, 
    "last_name":login_data.last_name,"phone":login_data.phone, "email":login_data.email }
    
    password = await hashing.encode_password(login_data.password)
    values["password"] = password.decode("utf-8") 
    print(values)
    token = access_security.create_access_token(subject=values)
    print (token)
    values["api_token"] = token

    query = """INSERT INTO "UniversityStaff" (first_name, last_name, middle_name,
    phone, email, password,  api_token) 
    SELECT :first_name,:middle_name,:last_name, :phone, :email, :password, :api_token
    WHERE
    NOT EXISTS (
    SELECT CAST(:phone AS VARCHAR) FROM "UniversityStaff" WHERE phone = :phone) 
    RETURNING  id"""
    
    id = await database.execute(query=query, values=values)
    response.delete_cookie(key="access_token")
    if id != None:
        #response.set_cookie(key="access_token", value = values["api_token"])
        return  {"message": "Come to the dark side, we have cookies", "access_token":request.cookies.get('access_token'), "values":values}
    return {"message": "Пользователь с таким телефоном или почтой уже существует"}

@auth_router.post("/sign_up/student/", summary="")
async def auth(response: Response,request: Request, login_data:LoginData ): 
    values = { "first_name":login_data.first_name,"middle_name":login_data.middle_name, 
    "last_name":login_data.last_name,"phone":login_data.phone, "email":login_data.email }
    password = await hashing.encode_password(login_data.password)
    values["password"] = password.decode("utf-8") 

    query = """INSERT INTO "Student" (first_name, last_name, middle_name,
    phone, email, password) 
    SELECT :first_name,:middle_name,:last_name, :phone, :email, :password
    WHERE
    NOT EXISTS (
    SELECT CAST(:phone AS VARCHAR ) FROM "Student" WHERE phone = :phone)
    RETURNING  id"""
    
    id = await database.execute(query=query, values=values)
    response.delete_cookie(key="access_token")
    if id != None:
        return  {"values":values}
    return {"message": "Пользователь с таким телефоном или почтой уже существует"}


#JSONResponse(status_code=404, content = {"description": "Not found","request_date":datetime.datetime.now().timestamp()
@auth_router.post("/sign_in/staff/", summary="")
async def sign_in(email:str, password:str)->UniversityStaffRecord: 
    query = staff_table.select().where(staff_table.c.email == email)
    staff = await database.fetch_one(query)
    if await hashing.check_password(password,staff["password"]) == True:
        return staff
    else:
        return staff["password"]

#JSONResponse(status_code=404, content = {"description": "Not found","request_date":datetime.datetime.now().timestamp()
@auth_router.post("/sign_in/student/", summary="")
async def sign_in(email:str, password:str)->Student: 
    query = staff_table.select().where(staff_table.c.email == email)
    staff = await database.fetch_one(query)
    if await hashing.check_password(password,staff["password"]) == True:
        return staff
    else:
        return staff["password"]

@auth_router.post("/logout/", summary="")
async def logout() -> UniversityStaff: 
    return UniversityStaff

async def refresh_token (token:JwtAuthorizationCredentials = Security(access_security)) -> UniversityStaffRecord:
    query = staff_table.select().where(staff_table.c.api_token == token)
    staff = await database.fetch_one(query)
    return staff   

@auth_router.get("/whoami/", summary="")
async def whoami(token:JwtAuthorizationCredentials = Security(access_security)): 
    return token
