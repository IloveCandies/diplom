from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db.settings import SQLALCHEMY_DATABASE_URL, CONNECT_ARGS
import databases


database = databases.Database(SQLALCHEMY_DATABASE_URL)

if CONNECT_ARGS == {}:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=CONNECT_ARGS)
    
metadata = MetaData()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
