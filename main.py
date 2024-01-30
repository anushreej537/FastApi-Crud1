from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from user import api as UserAPI
from user import router as UserRouter

app = FastAPI()

app.include_router(UserAPI.app)
app.include_router(UserRouter.router)




register_tortoise(
    app,
    db_url="postgres://postgres:root@127.0.0.1/fastapi",
    modules={'models': ['user.models',]},
    generate_schemas=True,
    add_exception_handlers=True
)