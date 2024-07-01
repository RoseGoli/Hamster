from .models import config
from peewee import DoesNotExist

class conf:
    def fetch(index: str = None):
        try:
            find = config.select().dicts().get()
            if index:
                find = find[index]
        
        except DoesNotExist:
            conf.insertOrUpdateConfig()
            return conf.fetch(index)
        
        return find
    
    def insertOrUpdateConfig(**kwargs):
        try:
            record = config.get()
            query  = record.update(**kwargs)
            query.execute()
        except DoesNotExist:
            config.create(**kwargs)