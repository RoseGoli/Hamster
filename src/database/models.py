from peewee import *
from src.config import settings

mysqlDb = MySQLDatabase(
    'Manager',
    user     = settings.USER,
    password = settings.PASSWORD,
    host     = settings.HOST,
    port     = 3306,
    charset  = 'utf8mb4'
)

class BaseModel(Model):
    class Meta:
        database = mysqlDb

class users(BaseModel):
    user_id = BigIntegerField(primary_key=True)
    step    = TextField(null=True)


class accounts(BaseModel):
    user_id      = BigIntegerField(primary_key=True)
    name         = CharField(max_length=100)
    username     = CharField(max_length=100)
    url          = CharField(max_length=1000)
    last_login   = IntegerField(default=0)
    balance      = IntegerField(default=0)
    profit       = IntegerField(default=0)
    last_check   = IntegerField(default=0)
    session_file = CharField(max_length=100)

mysqlDb.connect()
mysqlDb.create_tables([users, accounts])