from fastapi import APIRouter,Request,Form,status
from . models import *
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi_login import LoginManager
from fastapi.responses import JSONResponse

SECRET = 'your-secret-key'
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
manager = LoginManager(SECRET, token_url='/auth/token')
templates = Jinja2Templates(directory = 'user/templates')


def verify_password(plan_password,hashed_password):
    return pwd_context.verify(plan_password,hashed_password)



def get_password_hash(password):
    return pwd_context.hash(password)

@router.get('/',response_class=HTMLResponse)
async def registration(request:Request):
    return templates.TemplateResponse('reg.html',{"request":request})

@router.post('/registration_form/', response_class=HTMLResponse)
async def reg_form(request:Request, full_name:str = Form(...),
                   email:str = Form(...),
                   phone:int = Form(...),
                   password:str = Form(...)):
    if await Person.filter(email = email).exists():
        return RedirectResponse('/', status_code=status.HTTP_302_FOUND)
    
    elif await Person.filter(phone = phone).exists():
        return RedirectResponse('/', status_code=status.HTTP_302_FOUND)
    
    else:
        await Person.create(name = full_name ,email = email 
                            ,phone = phone ,password = password)
        return RedirectResponse('/', status_code=status.HTTP_302_FOUND)
    

@manager.user_loader()
async def load_user(phone: str):# could also be an asynchronous function
    if await Person.exists(phone=phone):
        user =await Person.get(phone=phone)
        return user

# the python-multipart package is required to use the OAuth2PasswordRequestForm
@router.post('/login_form/')
async def login(request:Request, phone:str=Form(...), password:str=Form(...)):
    phone = phone

    user = await load_user(phone)  # we are using the same function to retrieve the user
    if not user:
        return {'user not registered'}
                          
    elif not verify_password(password,user.password):
        return {'invalid password'}
                
    access_token = manager.create_access_token(
        data=dict(sub=phone)

    )
    print(access_token)
    return RedirectResponse('/table/',status_code=status.HTTP_302_FOUND)
    # return {'access_token': access_token, 'token_type': 'bearer'}

@router.get('/table/',response_class=HTMLResponse)
async def data_show(request:Request):
    person_obj = await Person.all()
    return templates.TemplateResponse('table.html', {'request':request ,
                                                     'person_obj':person_obj} )

@router.get('/delete/{id}/',response_class=HTMLResponse)
async def delete_data(request:Request,id:int):
    data=await Person.get(id=id).delete()
    print(data)
    # data.delete()
    return RedirectResponse('/table/', status_code=status.HTTP_302_FOUND)

    
@router.get('/update_id/{id}', response_class=HTMLResponse)
async def update_id(request:Request,id:int):
    data = await Person.get(id=id)
    return templates.TemplateResponse('update.html',{'request':request,
                                                      'data':data})

@router.post('/update_form/' , response_class=HTMLResponse)
async def update_data(request:Request,id:int=Form(...), full_name:str=Form(...)
                      , email:str=Form(...), phone:int=Form(...)):
    data = await Person.get(id=id)
    await Person.filter(id=id).update( name=full_name, email=email, phone=phone )
    return RedirectResponse('/table/',status_code=status.HTTP_302_FOUND)

@router.get('/login', response_class=HTMLResponse)
async def login(request:Request):
    return templates.TemplateResponse('login.html',{'request':request})