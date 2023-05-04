from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

#
from routers.groups import groups_router
from routers.user import user_router 
from routers.university import university_router 
from routers.oop import oop_router 
from routers.shedule_plan import shedule_plan_router
from routers.disciplines_in_shedule_plan import shedule_plan_disciplines_router
from routers.disciplines_in_student_education import student_education_disciplines_router
from routers.student_education import student_education_router
from routers.university_staff import university_staff_router
from routers.student import student_router
from routers.favorite_list import favorite_list_router
#
from db.init import database

from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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


app.include_router(groups_router,tags=["Методы группы / Group methods"])
app.include_router(user_router,tags=["Методы пользователя / User methods"])
app.include_router(university_router,tags=["Методы ВУЗА / University methods"])
app.include_router(university_staff_router,tags=["Сотрудники ВУЗА / University sraff methods"])
app.include_router(oop_router,tags=["ООП Вуза / University Education Programm"])
app.include_router(shedule_plan_router,tags=["Учебный план / Shedule Plan"])
app.include_router(shedule_plan_disciplines_router,tags=["Дисциплины учебных планов / Disciplines in shedule plans"])
app.include_router(student_education_disciplines_router,tags=["Дисциплины студентов / Disciplines in student education"])
app.include_router(student_router,tags=["Студенты / Students"])
app.include_router(favorite_list_router,tags=["Список избранного студента / Student favorite list"])
  



@app.get("/")
async def root():
    return {"message": "Hello World"}
