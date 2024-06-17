from .models import accounts

class acc:
    def fetch(value: str|int):
        try:
            if isinstance(value, int):
                find = accounts.get(accounts.user_id == value)
            elif isinstance(value, str):
                find = accounts.get(accounts.session_file == value)
        except Exception as e:
            find = {}
        
        return find
    
    def insertOrUpdateAcc(user_id, **kwargs):
        return (
            accounts
                .insert(user_id=user_id, **kwargs)
                .on_conflict('replace')
                .execute()
        )