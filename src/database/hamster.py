from .models import hamsterKombat
from peewee import DoesNotExist

class hamster:
    def fetch(value: str|int):
        try:
            if isinstance(value, int):
                find = hamsterKombat.get(hamsterKombat.user_id == value)
            elif isinstance(value, str):
                find = hamsterKombat.get(hamsterKombat.session_file == value)
        except Exception as e:
            find = {}
        
        return find
    
    def insertOrUpdateHamster(user_id, **kwargs):
        try:
            record = hamsterKombat.get(hamsterKombat.user_id == user_id)
            query  = hamsterKombat.update(**kwargs).where(hamsterKombat.user_id == user_id)
            query.execute()
        except DoesNotExist:
            hamsterKombat.create(user_id=user_id, **kwargs)