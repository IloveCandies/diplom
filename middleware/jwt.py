from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer

#Вынести все контстанты в settigs
JWT_SECRET_KEY = ""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
access_security = JwtAccessBearer(secret_key="secret_key", auto_error=True,access_expires_delta=None,refresh_expires_delta=None)
