from pydantic import BaseModel

#Create the user model
class User(BaseModel):
    email:str
    password:str