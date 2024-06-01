from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from config.database import  engine, Base

#Import middlewares
from middlewares.error_handler import ErrorHandler

#Include router
from routers.movie_router import movie_router
from routers.user_router import user_router

#+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+
#Create app
app = FastAPI()
app.title = 'My project using FastApi'
app.version = '0.0.1'
#Add errorHandler
app.add_middleware(ErrorHandler)
#include router
app.include_router(movie_router)
app.include_router(user_router)


#+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+
#Create DataBase
Base.metadata.create_all(bind=engine)


#--------------------------------
@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')
