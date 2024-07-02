import random
import asyncio
import traceback

from time import time
from src.config import settings
from src.database.acc import acc
from src.utils.logger import logger
from .telegramApp import TelegramApp
from games.hamster.tapper import Tapper
from src.database.hamster import hamster
from src.utils.scripts import getSessions
from src.utils.scripts import parse_webapp_url

async def handleSession(session, bot: str, url: str, start_param: str = None):
    try:
        if bot == 'hamster_kombat_bot':
            search = acc.fetch(str(session))

            if time() - search.get('hamsterKombat', {}).get('last_login', 0) >= settings.RENEW_AUTH:
                app = TelegramApp(session)
                await app.connect()

                info = (await app.getClient().get_me())

                await app.resove_peer(bot)

                url = await app.get_web_data(
                    bot         = bot,
                    url         = url,
                    start_param = start_param,
                    raw_url     = True
                )

                acc.insertOrUpdateHamster(
                    user_id      = info.id,
                    name         = ' '.join(filter(None, [info.first_name, info.last_name])),
                    username     = info.username,
                    phone_number = info.phone,
                    session_file = session
                )

                if url:
                    hamster.insertOrUpdateHamster(
                        user_id      = info.id,
                        url          = url,
                        last_login   = time()
                    )
                
                hamster_client = Tapper(session)
                new_token      = await hamster_client.login(parse_webapp_url(url))
                token          = new_token if new_token != False else hamster.fetch(info.id)['token']

                while not token:
                    token = hamster_client.login(parse_webapp_url(url))
                    sleep = random.randint(1, 10)
                    logger.warning(f"{session} | sleep {sleep}sec befor token cache!")
                    await asyncio.sleep(sleep)

                hamster.insertOrUpdateHamster(
                    user_id = info.id,
                    token   = token
                )

                await app.disconnect()
    except Exception as e:
        print(traceback.format_exc())
        pass

async def connectAndCacheClients(bot: str, url: str, start_param: str = None):
    sessions = getSessions()
    tasks = [
        handleSession(session, bot, url, start_param)
        for session in sessions
    ]
    await asyncio.gather(*tasks)