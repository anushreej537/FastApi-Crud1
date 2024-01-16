from tortoise.models import Model
from tortoise import Tortoise,fields

class User(Model):
    id = fields.IntField(pk = True)
    name = fields.CharField(200)
    email = fields.CharField(200)
    phone = fields.IntField()
    password = fields.CharField(250)


Tortoise.init_models(['user.models'],'models')
    
