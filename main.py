from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse

from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

from typing import Coroutine, Optional, List

from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

from config.database import Session, engine, Base
from models.movie import Movie	as MovieModel

from fastapi.encoders import jsonable_encoder


#+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+
#Create app
app = FastAPI()
app.title = 'My project using FastApi'
app.version = '0.0.1'
#+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+

#+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+
#Create DataBase
Base.metadata.create_all(bind=engine)
#+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+

#+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+
#Create routes

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) :
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(status_code=403,detail='Credenciales inválidas' )


class User(BaseModel):
    email:str
    password:str


class Movie(BaseModel):
    id: Optional[int] = None
    title:str = Field( min_length=5 , max_length=15)
    overview:str = Field( min_length=15 , max_length=50 )
    year:int =  Field( le=2022 )
    rating:float = Field(ge=1, le=10.0)
    category:str = Field(min_length=5 , max_length=15)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
               {
                'id': 1,
                'title' : 'Crepusculo',
                'overview' : 'The twilight is almost better than sunday',
                'year' : '2022',
                'rating' : 9.5,
                'category' : 'Phantasy'
            }
            ]
        }
    }

movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "Avatar 2",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2015",
        "rating": 8.0,
        "category": "Acción"
    }
]

#--------------------------------
@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

#Login route--------------------
@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token:str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)

#--------------------------------
@app.get('/movies', tags=['movies'], response_model= List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies()-> List[Movie]:
    db = Session()      #Start a session
    result = db.query(MovieModel).all()        #Obtain all the data from the table
    db.close()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#--------------------------------
@app.get('/movies/{id}', tags=['movies'], response_model= Movie)
def get_movie(id:int = Path(ge=1, le=2000)):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    db.close()
    if not result:
       return JSONResponse(status_code=404, content={'message':'No se encontró ninguna película'})
    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#--------------------------------
@app.get('/movies/', tags=['movies'], response_model= List[Movie])
def get_movies_by_category(category:str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    db.close()
    if not result:
       return JSONResponse(status_code=404, content={'message':'No se encontró ninguna película'})
    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

    
    return JSONResponse(content=result)

#--------------------------------
#Add movies to the database.
@app.post('/movies', tags=['movies'], response_model= dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    
    return JSONResponse(status_code=201,content={'Message':'The movie has been registered.'})

#--------------------------------
@app.put('/movies/{id}', tags=['movies'], response_model= dict,  status_code=200)
def update_movie(id:int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404,content={'message':'No se encontró ninguna película'})
    
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category

    db.commit()    
    return JSONResponse( status_code=200, content={'Message':'The movie has been correctly updated.'})

#--------------------------------
@app.delete('/movies/{id}', tags=['movies'], response_model= dict,  status_code=200)
def delete_movie(id:int) ->dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404,content={'message':'No se encontró ninguna película'})
    
    db.delete(result)
    db.commit()

    return JSONResponse( status_code=200, content={'Message':'The movie has been correctly deleted.'})