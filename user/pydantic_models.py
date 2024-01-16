from pydantic import BaseModel


class Person(BaseModel):
    name:str
    email:str
    phone:int
    password:str