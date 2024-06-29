import asyncio

from aioclock.group import Group
from aioclock import AioClock, Every, OnStartUp

from src.config import settings
from src.utils.task import TaskManager
from games.hamster.tapper import Tapper
from src.utils.scripts import getSessions
from src.telegram.multiClients import connectAndCacheClients

group   = Group()
app     = AioClock()
manager = TaskManager()

app.include_group(group)

@app.task(trigger=OnStartUp())
async def startup():
    print('tasks on startup!')

    await connectAndCacheClients(
        'hamster_kombat_bot',
        'https://hamsterkombat.io',
        f"kentId{settings.OWNERS[0]}"
    )

    sessions = getSessions()
    tasks    = [asyncio.create_task(Tapper(session).run()) for session in sessions]
    await asyncio.gather(*tasks)

@group.task(trigger=Every(minutes=60))
async def every():
    print("Cache on Every 60 minutes")
    await connectAndCacheClients(
        'hamster_kombat_bot',
        'https://hamsterkombat.io',
        f"kentId{settings.OWNERS[0]}"
    )

@group.task(trigger=Every(minutes=120))
async def every():
    print("Daily on Every 60 minutes")

    sessions = getSessions()
    tasks    = [asyncio.create_task(Tapper(session).daily_events()) for session in sessions]
    await asyncio.gather(*tasks)