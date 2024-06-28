import sys
import asyncio
import traceback

from tasks import app
from src.telegram.client import getClient, startClient

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
        #await app.serve()
        await bot.run_until_disconnected()
        
    except asyncio.CancelledError:
        pass

    except KeyboardInterrupt:
        print("KeyboardInterrupt received, shutting down...")

    except Exception as err:
        print(f"An error occurred: {err}", exc_info=True)

    finally:
        await bot.disconnect()

if __name__ == '__main__':
    asyncio.run(main())