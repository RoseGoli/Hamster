from aioclock.group import Group
from aioclock import AioClock, Every, Once, OnShutDown, OnStartUp

from games.hamster.tapper import Tapper
from src.utils.scripts import getSessions
from src.telegram.multiClients import connectAndCacheClients

group = Group()
app   = AioClock()
app.include_group(group)

@app.task(trigger=OnStartUp())
async def startup():
    print('tasks on startup!')

    await connectAndCacheClients(
        'hamster_kombat_bot',
        'https://hamsterkombat.io',
        'kentId1692387237'
    )


@group.task(trigger=Every(minutes=60))
async def every():
    print("Cache on Every 60 minutes")
    await connectAndCacheClients(
        'hamster_kombat_bot',
        'https://hamsterkombat.io',
        'kentId1692387237'
    )

@group.task(trigger=Every(minutes=60))
async def every():
    print("Daily on Every 60 minutes")
    for session in getSessions():
        hamster_client = Tapper(session)
        await hamster_client.daily_events()