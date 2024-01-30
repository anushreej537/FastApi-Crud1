from fastapi import APIRouter
from . models import *
from .pydantic_models import Table,Del_data,updateuser,Person_data,LoginUser,Token
from passlib.context import CryptContext
from fastapi_login import LoginManager
from fastapi.responses import JSONResponse

SECRET = 'your-secret-key'
app = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
manager = LoginManager(SECRET, token_url='/auth/token')



def verify_password(plan_password,hashed_password):
    return pwd_context.verify(plan_password,hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@manager.user_loader()
async def load_user(email: str):# could also be an asynchronous function
    if await Person.exists(email=email):
        user =await Person.get(email=email)
        return user

# the python-multipart package is required to use the OAuth2PasswordRequestForm
@app.post('/auth/token')
async def login(data: LoginUser):
    email = data.email

    user = await load_user(email)  # we are using the same function to retrieve the user
    if not user:
        return JSONResponse({"status":False, 'message':'user not registered'},
                            status_code=403)
    elif not verify_password(data.password,user.password):
        return JSONResponse({'status':False, 'message':'invalid password'},
                            status_code=403)
    
    access_token = manager.create_access_token(
        data=dict(sub=email)

    )
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.post("/register/")
async def ragistration(data:Person_data):
    if await Person.exists(phone=data.phone):
        return {"status":False, "message":"Phone Number already exists"}
    elif await Person.exists(email=data.email):
        return {"status":False, "message":"Email already exists"}
    else:
        user_obj = await Person.create(name=data.name,email=data.email,phone=data.phone,
                                     password=get_password_hash(data.password))
        return user_obj
    

@app.post('/table')
async def table_data(data:Table):
    user_data = await User.filter(id=data.id)
    return {'user_data':user_data}


@app.delete('/deldata')
async def delete_data(data:Del_data):
    await User.get(id=data.id).delete()
    return {"messsage" : 'user delete successfully'}

@app.put("/updatedata")
async def update_user(data:updateuser):
    user_obj = await User.get(id=data.id)
    if not user_obj:
        return {"status":False, "message":"User Not found"}
    else:
        user = User.filter(id=data.id).update(name=data.name,email=data.email,
                                              phone=data.phone)
        return {"status":True, "message":"user update sucessfully"}