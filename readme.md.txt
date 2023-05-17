#uvicorn main:app --runserver

#Для миграции на sqllite

Поменять на

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)