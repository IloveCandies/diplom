import hashlib
import os
from hashlib import blake2b 
# подробней https://docs.python.org/3/library/hashlib.html
from hmac import compare_digest
SECRET_KEY = b'sdfwrew4342rwrwdsfer234'
AUTH_SIZE = 16


async def encode_password(password:str):
    user_password = blake2b(digest_size=AUTH_SIZE, key=SECRET_KEY)
    return user_password.hexdigest().encode('utf-8')

async def check_password(input_pass:str, user_password:str):
    encoded_input_pass = await encode_password(input_pass)
    return compare_digest(encoded_input_pass,user_password.encode('utf-8'))


