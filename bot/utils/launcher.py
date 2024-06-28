import os
import glob
import asyncio
import traceback

from itertools import cycle
from better_proxy import Proxy
from telethon import TelegramClient as Client

from bot.utils import logger
from bot.config import settings

from bot.core.tapper import Tapper
from bot.exceptions import InvalidSession


class SessionManager:
    def __init__(self, session_dir='sessions'):
        self.session_dir = session_dir

    def get_session_names(self) -> list[str]:
        session_files = glob.glob(f'{self.session_dir}/*.session')
        session_names = [os.path.splitext(os.path.basename(file))[0] for file in session_files]
        return session_names


class ProxyManager:
    @staticmethod
    def get_proxies() -> list[Proxy]:
        if settings.USE_PROXY_FROM_FILE:
            with open(file='bot/config/proxies.txt', encoding='utf-8-sig') as file:
                proxies = [Proxy.from_str(proxy=row.strip()).as_url for row in file]
        else:
            proxies = []
        return proxies


class TelegramClientManager:
    def __init__(self, session_dir='sessions'):
        if not settings.API_ID or not settings.API_HASH:
            raise ValueError("API_ID and API_HASH not found in the .env file.")
        
        self.api_id          = settings.API_ID
        self.api_hash        = settings.API_HASH
        self.session_manager = SessionManager(session_dir)
        self.tg_clients      = {}


    async def get_tg_clients(self) -> list[Client]:
        session_names = self.session_manager.get_session_names()

        if not session_names:
            raise FileNotFoundError("No session files found")
        
        self.tg_clients.update({
            session_name : Client(
                session  = f'sessions/{session_name}',
                api_id   = self.api_id,
                api_hash = self.api_hash
            )
            for session_name in session_names
            if session_name not in self.tg_clients
        })

        return list(self.tg_clients.values())
    
    async def get_tg_clients(self) -> list[Client]:
        session_names = self.session_manager.get_session_names()

        if not session_names:
            raise FileNotFoundError("No session files found")
        
        tg_clients = [
            Client(session=f'sessions/{session_name}', api_id=self.api_id, api_hash=self.api_hash,proxy=("socks5", '127.0.0.1', 9050) if settings.USE_TOR_PROXY else None)
            for session_name in session_names
        ]

        self.tg_clients = tg_clients
        return tg_clients
    
    async def connect_all_clients(self):
        if not self.tg_clients:
            await self.get_tg_clients()

        for client in self.tg_clients:
            try:
                if not client.is_connected():
                    await client.connect()
                    logger.info(f"Connected client: {client.session.filename}")
            except Exception:
                raise InvalidSession(client.session.filename)

    async def disconnect_all_clients(self):
        for client in self.tg_clients:
            if client.is_connected():
                await client.disconnect()
                logger.info(f"Disconnected client: {client.session.filename}")


class TaskRunner:
    def __init__(self, tg_clients: list[Client] = []):
        self.tasks         = []
        self.sessions      = []
        self.tg_clients    = tg_clients
        self.proxies       = ProxyManager.get_proxies()
        self.proxies_cycle = cycle(self.proxies) if self.proxies else None

    async def run_tapper_method(self, tg_client: Client, method_name: str, *args, **kwargs):
        try:
            tapper = Tapper(tg_client=tg_client)
            method = getattr(tapper, method_name)

            result = await method(*args, **kwargs)
            return result
        
        except InvalidSession:
            print(traceback.format_exc())
            logger.error(f"{tg_client.session.filename} | Invalid Session")
        
        except AttributeError:
            logger.error(f"{method_name} is not a valid method of Tapper")
        
        except Exception as e:
            logger.error(f"An error occurred: {e}")
        
        return False
    
    async def _collect_results(self) -> int:
        try:
            results = await asyncio.gather(*self.tasks, return_exceptions=True)
            return results
        except asyncio.CancelledError:
            logger.info("All tasks were cancelled")
            return 0
    
    async def run_tasks(self, method_name: str, return_results: bool = False, *args, **kwargs) -> int:
        if self.tasks != []:
            return 0
        
        if len(self.tg_clients) == 0:
            self.tg_clients = await TelegramClientManager().get_tg_clients()
        
        self.tasks = [
            asyncio.create_task(
                self.run_tapper_method(
                    tg_client   = tg_client,
                    method_name = method_name,
                    *args, **kwargs
                )
            ) for tg_client in self.tg_clients
        ]

        if return_results:
            result = await asyncio.create_task(self._collect_results())
        else:
            asyncio.create_task(self._collect_results())
            result = len(self.tasks)
        
        return result

    async def cancel_all_tasks(self):
        tasks_count = len(self.tasks)

        for task in self.tasks:
            task.cancel()
        
        self.tasks = []
        return tasks_count