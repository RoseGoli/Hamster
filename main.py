import sys
import asyncio
import traceback

from bot.config import settings
from bot.app import getClient

try:
    import bot.plugins as plugins
except ImportError:
    try:
        from . import plugins
    except ImportError:
        print(traceback.format_exc())
        print('could not load the plugins module', file=sys.stderr)
        exit(1)

async def main():
    bot = await getClient()
    await bot.start(bot_token = settings.TG_TOKEN)
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