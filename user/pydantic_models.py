from pydantic import BaseModel

class LoginUser(BaseModel):
    email:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str = 'bearer'


class Person_data(BaseModel):
    name:str
    email:str
    phone:int
    password:str

class Table(BaseModel):
    id : int
    
class Del_data(BaseModel):
    id : int

class updateuser(BaseModel):
    id:int
    name:str
    email:str
    phone:int
