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
    phone_number = CharField(max_length=50)
    session_file = CharField(max_length=100)

class hamsterKombat(BaseModel):
    user_id      = ForeignKeyField(accounts, backref='hamsterKombat')
    url          = CharField(max_length=1000)
    token        = CharField(max_length=500)
    last_login   = IntegerField(default=0)
    balance      = IntegerField(default=0)
    profit       = IntegerField(default=0)
    last_check   = IntegerField(default=0)

class config(BaseModel):
    hamsterKombat = BooleanField(default=False)

mysqlDb.connect()
mysqlDb.create_tables([users, config, accounts, hamsterKombat])