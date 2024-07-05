import random
import asyncio
import traceback

from time import time
from telethon import functions
from src.config import settings
from src.database.acc import acc
from src.utils.logger import logger
from .telegramApp import TelegramApp
from games.hamster.tapper import Tapper
from src.database.hamster import hamster
from src.utils.scripts import getSessions
from src.utils.scripts import parse_webapp_url, get_mobile_user_agent

async def handleSession(session, bot: str, url: str, start_param: str = None):
    try:
        if bot == 'hamster_kombat_bot':
            search = acc.fetch(session)
            timer  = search.get('hamsterKombat', {}).get('last_login', 0)
            token  = search.get('hamsterKombat', {}).get('token', False)

            if (time() - timer >= settings.RENEW_AUTH) or not token:

                app = TelegramApp(session)
                await app.connect()

                info = (await app.getClient().get_me())
                
                #await app.resove_peer(bot)
                await app.getClient()(functions.account.UpdateStatusRequest(
                    offline=False
                ))

                url = await app.get_web_data(
                    bot         = bot,
                    url         = url,
                    start_param = start_param,
                    raw_url     = True
                )

                acc.insertOrUpdate(
                    user_id      = info.id,
                    name         = ' '.join(filter(None, [info.first_name, info.last_name])),
                    username     = info.username if (hasattr(info, 'username') and info.username != None) else None,
                    phone_number = info.phone,
                    session_file = session,
                    user_agent   = get_mobile_user_agent()
                )

                if url:
                    hamster.insertOrUpdate(
                        user_id      = info.id,
                        url          = url,
                        last_login   = time()
                    )
                
                    hamster_client = Tapper(session)
                    new_token      = await hamster_client.login(parse_webapp_url(url))
                    token          = new_token if new_token != False else hamster.fetch(info.id)['token']

                    while not token:
                        token = await hamster_client.login(parse_webapp_url(url))
                        sleep = random.randint(1, 10)
                        logger.warning(f"{session} | sleep {sleep}sec befor token cache!")
                        await asyncio.sleep(sleep)

                    hamster.insertOrUpdate(
                        user_id = info.id,
                        token   = token
                    )

                await app.disconnect()
    except Exception as e:
        print(traceback.format_exc())
        pass

async def connectAndCacheClients(bot: str, url: str, start_param: str = None):
    sessions = getSessions()
    tasks    = [
        asyncio.create_task(handleSession(session, bot, url, start_param))
        for session in sessions
    ]

    await asyncio.gather(*tasks)