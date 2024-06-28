from .models import hamsterKombat
from peewee import DoesNotExist

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