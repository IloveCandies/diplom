from hashlib import blake2b,pbkdf2_hmac
from os import urandom
import uuid
# подробней https://docs.python.org/3/library/hashlib.html

from hmac import compare_digest
SECRET_KEY = b'sdfwrew4342rwrwdsfer234'

AUTH_SIZE = 16


async def encode_password(password:str,salt = uuid.uuid4().hex):
    user_password = pbkdf2_hmac('blake2b', password.encode(), salt.encode(), 100000)
    return user_password.hex(),salt

async def check_password(input_pass:str, user_password:str, salt:str):
    encoded_input_pass = await encode_password(input_pass,salt)
    return compare_digest(encoded_input_pass[0],user_password)


