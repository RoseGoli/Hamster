import os

from config import settings
from utils.logger import logger
from telethon import TelegramClient as Client

async def register_sessions() -> None:
    API_ID   = settings.API_ID
    API_HASH = settings.API_HASH

    if not API_ID or not API_HASH:
        raise ValueError("API_ID and API_HASH not found in the .env file.")

    session_name = input('\nEnter the session name (press Enter to exit): ')

    if not session_name:
        return None
    
    if not os.path.exists(settings.SESSION_PATH):
        os.mkdir(settings.SESSION_PATH)
    
    session = Client(
        session  = os.path.join(settings.SESSION_PATH, session_name),
        api_id   = API_ID,
        api_hash = API_HASH
    )

    async with session:
        user_data = await session.get_me()
    
    logger.success(f'Session added successfully @{user_data.username} | {user_data.first_name} {user_data.last_name}')