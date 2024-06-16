from .models import users

class db:
    def upsert(self, user_id, step = None):
        return (
            users
                .replace(user_id=user_id, step=step)
                .execute()
        )