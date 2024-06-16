import os
import asyncio

from utils.logger import logger
from exceptions import InvalidSession
from utils.scripts import parse_webapp_url
from telethon import TelegramClient as Client, functions

class TelegramApp:
    def __init__(self, client: Client) -> None:
        self.client  = client
        self.session = os.path.basename(client.session.filename)

    async def connect(self):
        """Connects to the Telegram client."""
        try:
            if not self.client.is_connected():
                await self.client.connect()
                logger.info(f"Connected client: {self.session}")
        except Exception as error:
            logger.error(f"Error connecting client: {self.session}, {str(error)}")
            raise InvalidSession(self.session)

    async def disconnect(self):
        """Disconnects from the Telegram client."""
        try:
            if self.client.is_connected():
                await self.client.disconnect()
                logger.info(f"Disconnected client: {self.session}")
        except Exception as error:
            logger.error(f"Error disconnecting client: {self.session}, {str(error)}")
            raise Exception(self.session)
        
    async def join_channel(self, channel: str) -> bool:
        """Joins a Telegram channel."""
        try:
            await self.connect()
            await self.client(functions.channels.JoinChannelRequest(channel))
            await self.disconnect()
            return True
        except Exception as error:
            logger.error(f"{self.session} | Error during join: {error}")
            return False
    
    async def get_web_data(
        self, bot: str, url: str, platform: str = 'android', 
        start_param: str = None, only_url: bool = False
    ) -> str:
        """Fetches web data from a bot."""
        try:
            await self.connect()

            web_view = await self.client(
                functions.messages.RequestWebViewRequest(
                    peer          = bot,
                    bot           = bot,
                    platform      = platform,
                    from_bot_menu = False,
                    start_param   = start_param,
                    url           = url
                )
            )

            await self.disconnect()

            auth_url    = web_view.url
            tg_web_data = parse_webapp_url(auth_url)
            
            if only_url:
                return auth_url
            
            return tg_web_data
        
        except Exception as error:
            logger.error(f"{self.session} | Failed to get web data: {error}")
            await asyncio.sleep(delay=3)
            return ""