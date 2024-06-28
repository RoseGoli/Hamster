import asyncio
from src.telegram.multiClients import connectAndCacheClients

asyncio.run(connectAndCacheClients(
    'hamster_kombat_bot',
    'https://hamsterkombat.io',
    'kentId1692387237'
))