import asyncio

from aioclock.group import Group
from aioclock import AioClock, Every, OnStartUp

from src.config import settings
from src.utils.logger import logger
from games.hamster.tapper import Tapper
from src.utils.scripts import getSessions
from src.telegram.multiClients import connectAndCacheClients

group = Group()
app   = AioClock()
app.include_group(group)

@app.task(trigger=OnStartUp())
async def startup():
    logger.info('tasks on startup!')

    await connectAndCacheClients(
        'hamster_kombat_bot',
        'https://hamsterkombat.io',
        f"kentId{settings.OWNERS[0]}"
    )

    sessions = getSessions()
    referal  = [asyncio.create_task(Tapper(session).add_referral()) for session in sessions]

    sessions = getSessions()
    tasks    = [asyncio.create_task(Tapper(session).run()) for session in sessions]
    
    allJobs  = referal + tasks

    await asyncio.gather(*allJobs)

@group.task(trigger=Every(minutes=60))
async def every():
    logger.info("Cache on Every 60 minutes")
    await connectAndCacheClients(
        'hamster_kombat_bot',
        'https://hamsterkombat.io',
        f"kentId{settings.OWNERS[0]}"
    )

@group.task(trigger=Every(minutes=120))
async def every():
    logger.info("Daily on Every 120 minutes")
    
    sessions = getSessions()
    tasks    = [asyncio.create_task(Tapper(session).daily_events()) for session in sessions]
    await asyncio.gather(*tasks)