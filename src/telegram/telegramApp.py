import os
import json
import shutil
import asyncio

from src.config import settings
from src.utils.logger import logger
from src.utils.scripts import parse_webapp_url
from telethon import TelegramClient as Client, functions

class TelegramApp:
    def __init__(self, session_name: str) -> None:
        self.client  = None
        self.session = session_name

        self.getClient()

    def getClient(self):
        if self.client:
            return self.client
        
        data_path = f'{settings.SESSION_PATH}/{self.session}.json'
        
        if os.path.exists(data_path):
            with open(data_path, 'r') as file:
                session_data = json.load(file)
        else:
            session_data = {}

        api_id      = session_data.get('api_id', settings.API_ID)
        api_hash    = session_data.get('api_hash', settings.API_HASH)
        self.client = Client(session=f'sessions/{self.session}', api_id=api_id, api_hash=api_hash)

        return self.client

    async def connect(self):
        """Connects to the Telegram client."""
        try:
            if not self.client.is_connected():
                await self.client.connect()

                if not await self.client.is_user_authorized():
                    logger.error(f"Bad session: {self.session}")
                    await self.disconnect()
                    self.move_bad_session_files()

                else:
                    logger.info(f"Connected client: {self.session}")
        except Exception as error:
            logger.error(f"Error connecting client: {self.session}, {str(error)}")
            raise Exception(self.session)

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
        start_param: str = None, raw_url: bool = False
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
            
            if raw_url:
                return auth_url
            
            return tg_web_data
        
        except Exception as error:
            logger.error(f"{self.session} | Failed to get web data: {error}")
            await asyncio.sleep(delay=3)
            return ""
        
    def move_bad_session_files(self):
        extensions  = ['.session', '.json']
        moved_files = []

        for ext in extensions:
            src = os.path.join(settings.SESSION_PATH, f"{self.session}{ext}")
            dst = os.path.join(settings.BAD_SESSIONS_PATH, f"{self.session}{ext}")

            if os.path.exists(src):
                shutil.move(src, dst)
                moved_files.append(src)

        if moved_files:
            logger.error(f"Session {self.session} moved to bad sessions: {moved_files}")
            raise Exception('not authorized')