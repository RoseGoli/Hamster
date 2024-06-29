from src.database.acc import acc
import json

print(json.dumps(acc.fetch(6447374319), indent=4))
#print(acc.fetch(6447374319))