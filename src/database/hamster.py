from .models import hamsterKombat
from peewee import DoesNotExist
from peewee import fn

class hamster:
    def fetch(user_id: str|int):
        try:
            find = hamsterKombat.select().where(hamsterKombat.user_id == user_id).dicts().get()
        except DoesNotExist:
            find = {}
        
        return find
    
    def insertOrUpdateHamster(user_id, **kwargs):
        try:
            record = hamsterKombat.get(hamsterKombat.user_id == user_id)
            query  = hamsterKombat.update(**kwargs).where(hamsterKombat.user_id == user_id)
            query.execute()
        except DoesNotExist:
            hamsterKombat.create(user_id=user_id, **kwargs)

    def total_info():
        total_balance = hamsterKombat.select(fn.SUM(hamsterKombat.balance)).scalar()
        total_profit  = hamsterKombat.select(fn.SUM(hamsterKombat.profit)).scalar()
        
        return {
            'balance' : total_balance,
            'profit'  : total_profit
        }
