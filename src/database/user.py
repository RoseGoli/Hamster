from .models import users

class user:
    def get(user_id):
        return users.get(users.user_id == user_id)
    
    def insertOrUpdateUser(user_id, step = None):
        return (
            users
                .insert(user_id=user_id, step=step)
                .on_conflict('replace')
                .execute()
        )