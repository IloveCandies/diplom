from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers.auth import router as auth_router
from routers.groups import groups_router
from routers.user import user_router 
from routers.university import university_router 
from routers.oop import oop_router 
from routers.shedule_plan import shedule_plan_router
from routers.disciplines_in_shedule_plan import shedule_plan_disciplines_router
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

app.include_router(auth_router,tags=["Авторизация"])
app.include_router(groups_router,tags=["Методы группы / Group methods"])
app.include_router(user_router,tags=["Методы пользователя / User methods"])
app.include_router(university_router,tags=["Методы ВУЗА / University methods"])
app.include_router(oop_router,tags=["ООП Вуза / University Education Programm"])
app.include_router(shedule_plan_router,tags=["Учебный план / Shedule Plan"])
app.include_router(shedule_plan_disciplines_router,tags=["Дисциплины учебных планов / Disciplines in shedule plans"])



@app.get("/")
async def root():
    return {"message": "Hello World"}
