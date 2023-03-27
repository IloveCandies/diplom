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




upstream app_server {
    server unix:/home/fastapi-user/fastapi-nginx-gunicorn/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;

    # add here the ip address of your server
    # or a domain pointing to that ip (like example.com or www.example.com)
    
    keepalive_timeout 10;

    access_log /home/transfer/fastapi/fastapi-nginx-gunicorn/logs/nginx-access.log;
    error_log /home/transfer/fastapi/fastapi-nginx-gunicorn/logs/nginx-error.log;

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
                        
        if (!-f $request_filename) {
            proxy_pass http://app_server;
            break;
        }
	}
}
# Основные настройки
        listen 80 default_server;
        listen [::]:80 default_server;
        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;
        server_name www.transfer.kemsu.ru;
        location / {
                # вначале попытаемся обработать запрос как файл,
                # затем как каталог, затем вернём ошибку 404
                try_files $uri $uri/ =404;
        }
        
        # проксируем запрос /xxx на web1
        location /xxx {
                proxy_pass http://web1/test/;
        }
        
        # проксируем запрос /yyy на web2
        location /yyy {
                proxy_pass http://web2/test/;
        }
}


upstream app_server {
    server unix:/home/fastapi-user/fastapi-nginx-gunicorn/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80 default_server;
    listen [::]:80 default_server;

    # add here the ip address of your server
    # or a domain pointing to that ip (like example.com or www.example.com)
    server_name www.transfer.kemsu.ru;

    keepalive_timeout 10;
    client_max_body_size 4G;

    access_log /home/fastapi-user/fastapi-nginx-gunicorn/logs/nginx-access.log;
    error_log /home/fastapi-user/fastapi-nginx-gunicorn/logs/nginx-error.log;
    
    location /xxx {
        # Управление заголовками на прокси сервере
        proxy_set_header X-Scheme http;
        proxy_set_header X-Forwarded-Proto http;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Real-PORT $remote_port;
        proxy_set_header X-Real-IP $remote_addr;
        # настройка буфера для прокси сервера
        proxy_buffering on;
        proxy_buffer_size 8k;
        proxy_buffers 8 8k;
        proxy_pass http://web1/test/;
        
        }
}














http {
  server {
    listen 80;
    client_max_body_size 4G;

    server_name www.transfer.kemsu.ru;

    location /api {
      proxy_set_header Host $http_host;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection $connection_upgrade;
      proxy_redirect off;
      proxy_buffering off;
      proxy_pass http://uvicorn;
    }

  map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
  }

upstream uvicorn {
    server unix:/home/fastapi-user/fastapi-nginx-gunicorn/run/gunicorn.sock fail_timeout=0;
        }
    }
}