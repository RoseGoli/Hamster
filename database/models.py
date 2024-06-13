from peewee import *
from config import settings

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
    phone_number = BigIntegerField(primary_key=True)
    user_id      = BigIntegerField()
    login_at     = TimestampField()
    settings     = CharField()
    balance      = IntegerField(default=0)
    profit       = IntegerField(default=0)
    last_check   = IntegerField(default=0)

mysqlDb.connect()
mysqlDb.create_tables([users, accounts])