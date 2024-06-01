from jwt import encode, decode

import os
from dotenv import load_dotenv

llaveSecreta:str = str(os.getenv('SECRET_KEY'))

def create_token(data:dict):
    token:str = encode(payload=data, key=llaveSecreta, algorithm='HS256')
    return token

def validate_token(token:str) -> dict:
    data: dict = decode(token, key=llaveSecreta, algorithms=['HS256']) 
    return data