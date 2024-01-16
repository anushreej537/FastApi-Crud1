from fastapi import APIRouter
from . models import *
from .pydantic_models import Person
from passlib.context import CryptContext



app = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plan_password,hashed_password):
    return pwd_context.verify(plan_password,hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


@app.post("/")
async def ragistration(data:Person):
    phone_number = str(data.phone)
    if len(phone_number) != 10:
        return {"status":False, "message":"Phone Number Invalid"}


    if await User.exists(phone=phone_number):
        return {"status":False, "message":"Phone Number already exists"}
    elif await User.exists(email=data.email):
        return {"status":False, "message":"Email already exists"}
    else:
        user_obj = await User.create(name=data.name,email=data.email,phone=phone_number,
                                     password=get_password_hash(data.password))
        return user_obj