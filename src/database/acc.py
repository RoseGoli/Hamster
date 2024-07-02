from .models import accounts, hamsterKombat
from peewee import DoesNotExist, IntegrityError

class acc:
    def fetch(value: str | int):
        try:
            find           = {}
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
            
        except DoesNotExist as e:
            result = {}
        
        return result
    
    def insertOrUpdate(user_id, **kwargs):
        try:
            record = accounts.get(accounts.user_id == user_id)
            for key, value in kwargs.items():
                setattr(record, key, value)
            record.save()
        except DoesNotExist:
            try:
                accounts.create(user_id=user_id, **kwargs)
            except IntegrityError as e:
                print(f"IntegrityError: {e}")
                raise