from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.auth import router as aut_router
from routers.groups import router as groups_router
from routers.user import router as user_router
from routers.university import router as university_router

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(aut_router,tags=["Авторизация"])
app.include_router(groups_router,tags=["Методы группы / Group methods"])
app.include_router(user_router,tags=["Методы пользователя / User methods"])
app.include_router(university_router,tags=["Методы ВУЗА / University methods"])

@app.get("/")
async def root():
    return {"message": "Hello World"}
