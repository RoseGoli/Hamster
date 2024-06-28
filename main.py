import sys
import asyncio
import traceback

from src.telegram.client import getClient, startClient
from src.telegram.multiClients import connectAndCacheClients

from aioclock.group import Group
from aioclock import AioClock, Every, Once, OnShutDown, OnStartUp

group = Group()
app   = AioClock()
app.include_group(group)

try:
    import plugins as plugins
except ImportError:
    try:
        from . import plugins
    except ImportError:
        print(traceback.format_exc())
        print('could not load the plugins module', file=sys.stderr)
        exit(1)

async def main():
    bot = await getClient()
    await startClient()
    bot.parse_mode = 'html'

    try:
        await plugins.init(bot)
        await app.serve()
        await bot.run_until_disconnected()
        
    except asyncio.CancelledError:
        pass

    finally:
        await bot.disconnect()

@app.task(trigger=OnStartUp())
async def startup():
    print('tasks on startup!')

    await connectAndCacheClients(
        'hamster_kombat_bot',
        'https://hamsterkombat.io',
        'kentId1692387237'
    )


@group.task(trigger=Every(minutes=1))
async def every():
    print("Task on Every 1 minutes")
    await connectAndCacheClients(
        'hamster_kombat_bot',
        'https://hamsterkombat.io',
        'kentId1692387237'
    )

if __name__ == '__main__':
    asyncio.run(main())