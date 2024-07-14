import asyncio

from aioclock.group import Group
from aioclock import AioClock, Every, Once

from src.config import settings
from src.utils.logger import logger
from games.hamster.tapper import Tapper
from src.utils.scripts import getSessions
from src.telegram.multiClients import connectAndCacheClients

group = Group()
app   = AioClock()
app.include_group(group)

@app.task(trigger=Once())
async def once():
    logger.info('tasks on startup!')

    await connectAndCacheClients(
        'hamster_kombat_bot',
        'https://hamsterkombatgame.io',
        f"kentId{settings.OWNERS[0]}"
    )

    referal_tasks = [asyncio.create_task(Tapper(session).add_referral()) for session in getSessions()]
    tasks_tasks   = [asyncio.create_task(Tapper(session).run()) for session in getSessions()]
    daily_tasks   = [asyncio.create_task(Tapper(session).daily_events()) for session in getSessions()]
    all_jobs      = referal_tasks + tasks_tasks + daily_tasks

    await asyncio.gather(*all_jobs)

@group.task(trigger=Every(minutes=60))
async def every():
    logger.info("Cache on Every 60 minutes")
    await connectAndCacheClients(
        'hamster_kombat_bot',
        'https://hamsterkombatgame.io',
        f"kentId{settings.OWNERS[0]}"
    )

@group.task(trigger=Every(minutes=120))
async def every():
    logger.info("Daily on Every 120 minutes")
    
    sessions = getSessions()
    tasks    = [asyncio.create_task(Tapper(session).daily_events()) for session in sessions]
    await asyncio.gather(*tasks)