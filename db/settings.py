import os
SQLALCHEMY_DATABASE_URL = ""
CONNECT_ARGS = {}
try:
    SQLALCHEMY_DATABASE_URL  = os.environ['DATABASE_URL']
except:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./transfer.db"
    CONNECT_ARGS["check_same_thread"] = True
    print("Не удалось найти URL postgresql, будет создана sqllite БД ")