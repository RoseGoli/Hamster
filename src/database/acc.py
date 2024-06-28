from .models import accounts, hamsterKombat
from peewee import DoesNotExist

class acc:
    def fetch(value: str | int):
        try:
            query = (accounts
                .select(accounts, hamsterKombat)
                .join(hamsterKombat, on=(accounts.user_id == hamsterKombat.user_id))
            )
            
            if isinstance(value, int):
                find = query.where(accounts.user_id == value).dicts().get()
            
            elif isinstance(value, str):
                find = query.where(accounts.session_file == value).dicts().get()
            
        except DoesNotExist:
            find = {}
        
        return find
    
    def insertOrUpdateHamster(user_id, **kwargs):
        try:
            record = accounts.get(accounts.user_id == user_id)
            query  = accounts.update(**kwargs).where(accounts.user_id == user_id)
            query.execute()
        except DoesNotExist:
            accounts.create(user_id=user_id, **kwargs)