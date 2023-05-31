from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

#
from routers.groups import group_router 
from routers.university import university_router 
from routers.oop import oop_router 
from routers.shedule_plan import shedule_plan_router
from routers.disciplines_in_shedule_plan import shedule_plan_disciplines_router
from routers.disciplines_in_student_education import student_education_disciplines_router
from routers.student_education import student_education_router
from routers.university_staff import university_staff_router
from routers.student import student_router
from routers.favorite_list import favorite_list_router
from routers.discipline import discipline_router
from routers.auth import auth_router
from routers.test import test_router
#
from db.init import database
from fastapi_offline import FastAPIOffline

from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException


async def not_found_error(request: Request, exc: HTTPException):
    return RedirectResponse('https://fastapi.tiangolo.com')

exception_handlers = {404: not_found_error}
# root_path = "/api/v1"
app = FastAPI(exception_handlers=exception_handlers)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(auth_router,tags=["Авторизация"])

app.include_router(group_router,tags=["Методы группы"])
app.include_router(discipline_router,tags=["Дисциплины"])
app.include_router(oop_router,tags=["ООП"])
app.include_router(shedule_plan_router,tags=["Учебный план 90% сделано"])

app.include_router(favorite_list_router,tags=["Список избранного студента"])
app.include_router(student_router,tags=["Студенты в РАЗРАБОТКЕ 80%"])

app.include_router(university_router,tags=["Методы ВУЗА ПОКА НЕ РЕАЛИЗОВАННЫ "])
app.include_router(university_staff_router,tags=["Сотрудники ПОКА НЕ РЕАЛИЗОВАННЫ"])
app.include_router(test_router,tags=["ТЕСТ"])
  
  



@app.get("/")
async def root():
    return {"message": "Hello World"}
