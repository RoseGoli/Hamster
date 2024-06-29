from .models import accounts, hamsterKombat
from peewee import DoesNotExist

class acc:
    def fetch(value: str | int):
        try:
            account_fields = set(accounts._meta.fields.keys())
            hamster_fields = set(hamsterKombat._meta.fields.keys())
            
            query = (
                accounts
                .select(
                    accounts,
                    hamsterKombat
                )
                .join(hamsterKombat, on=(accounts.user_id == hamsterKombat.user_id))
            )
            
            if isinstance(value, int):
                find = query.where(accounts.user_id == value).dicts().get()
            
            elif isinstance(value, str):
                find = query.where(accounts.session_file == value).dicts().get()

            result       = {}
            hamster_info = {}
            
            for key, value in find.items():
                if key in hamster_fields and key != 'user_id':
                    hamster_info[key] = value
                else:
                    result[key] = value

            result['hamsterKombat'] = hamster_info
            
        except DoesNotExist:
            result = {}
        
        return result

    def insertOrUpdateHamster(user_id, **kwargs):
        try:
            record = accounts.get(accounts.user_id == user_id)
            query  = accounts.update(**kwargs).where(accounts.user_id == user_id)
            query.execute()
        except DoesNotExist:
            accounts.create(user_id=user_id, **kwargs)