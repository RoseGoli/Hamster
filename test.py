
import asyncio
from src.database.acc import acc
from src.telegram.multiClients import connectAndCacheClients

#print(getattr(acc.fetch('132'), 'last_login', 0))

asyncio.run(connectAndCacheClients('hamster_kombat_bot', 'https://hamsterkombat.io', 'kentId1692387237'))