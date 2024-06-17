import asyncio
import traceback

from time import time
from src.config import settings
from src.database.acc import acc
from .telegramApp import TelegramApp
from src.utils.scripts import getSessions

async def handleSession(session, bot: str, url: str, start_param: str = None):
    try:
        search = acc.fetch(session)

        if time() - getattr(search, 'last_login', 0) >= settings.RENEW_AUTH:
            app = TelegramApp(session)
            await app.connect()

            info = (await app.getClient().get_me())
            url  = await app.get_web_data(
                bot         = bot,
                url         = url,
                start_param = start_param,
                raw_url     = True
            )

            if url:
                acc.insertOrUpdateAcc(
                    user_id      = info.id,
                    name         = ' '.join(filter(None, [info.first_name, info.last_name])),
                    username     = info.username,
                    url          = url,
                    last_login   = time(),
                    session_file = session
                )

            await app.disconnect()
    except Exception as e:
        pass

async def connectAndCacheClients(bot: str, url: str, start_param: str = None):
    sessions = getSessions()
    tasks = [
        handleSession(session, bot, url, start_param)
        for session in sessions
    ]
    await asyncio.gather(*tasks)
