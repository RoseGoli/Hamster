import os
import sys
import asyncio
import traceback

from config import settings
from telegram.client import getClient, startClient

if not os.path.exists(settings.SESSION_PATH):
    os.mkdir(settings.SESSION_PATH)

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
        await bot.run_until_disconnected()
        
    except asyncio.CancelledError:
        pass

    finally:
        await bot.disconnect()

if __name__ == '__main__':
    asyncio.run(main())