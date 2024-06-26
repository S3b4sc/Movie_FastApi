from fastapi import APIRouter

from utils.jwt_manager import create_token
from fastapi.responses import JSONResponse

#import user schema or model
from schemas.user_schema import User

user_router = APIRouter()

#Login route--------------------
@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token:str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)
