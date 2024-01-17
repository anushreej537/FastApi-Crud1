from pydantic import BaseModel


class Person(BaseModel):
    name:str
    email:str
    phone:int
    password:str

class Table(BaseModel):
    id : int
    
class Del_data(BaseModel):
    id : int