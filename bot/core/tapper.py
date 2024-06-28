import os
import json
import asyncio
import aiohttp
import requests
import traceback

from bot.utils import logger
from bot.config import settings
from bot.exceptions import InvalidSession
from bot.utils.fingerprint import FINGERPRINT
from bot.utils.scripts import decode_cipher, find_best

from telethon.sync import functions
from telethon import TelegramClient as Client

from time import time
from random import randint
from urllib.parse import unquote
from datetime import datetime, timedelta

class Tapper:
    def __init__(self, tg_client: Client):
        self.token       = None
        self.headers     = {}
        self.client      = tg_client
        self.expire_date = datetime.now()
        self.session     = os.path.basename(tg_client.session.filename)

    def update_headers(self, new_headers):
        """
        Update the headers with new ones or add new headers.

        Args:
            new_headers (dict): A dictionary containing the new headers to add or update.

        Returns:
            None
        """
        self.headers.update(new_headers)
    
    async def send_request(self, method, url=None, endpoint=None, data=None, timeout=15, retries=3, backoff_factor=3):
        """
        Send an HTTP GET or POST request and return the response and any errors.
        
        Args:
            method (str): The HTTP method ('GET' or 'POST').
            url (str, optional): The full URL for the request.
            endpoint (str, optional): The endpoint to append to the base URL.
            data (dict, optional): The data to send with the request. For POST requests, this is the JSON data.
            timeout (int, optional): Timeout for the request in seconds. Defaults to 15 seconds.
            retries (int, optional): Number of retry attempts. Defaults to 3.
            backoff_factor (float, optional): Backoff multiplier for exponential backoff. Defaults to 1.
        
        Returns:
            tuple: A tuple containing the response object and an error message (if any).
        """

        headers = {
            'Accept'             : 'application/json',
            'Accept-Language'    : 'en-US,ru;q=0.9',
            'Content-Type'       : 'application/json',
            'Connection'         : 'keep-alive',
            'Origin'             : 'https://hamsterkombat.io',
            'Referer'            : 'https://hamsterkombat.io/',
            'Sec-Fetch-Dest'     : 'empty',
            'Sec-Fetch-Mode'     : 'cors',
            'Sec-Fetch-Site'     : 'same-site',
            'Sec-Ch-Ua'          : '"Android WebView";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'Sec-Ch-Ua-mobile'   : '?1',
            'Sec-Ch-Ua-platform' : '"Android"',
            "User-Agent"         : "Mozilla/5.0 (Linux; Android 11; SM-A305F Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/125.0.6422.147 Mobile Safari/537.36",
        }

        temp_header = headers.copy()
        temp_header.update(self.headers)

        if url:
            endpoint = url
        elif endpoint:
            endpoint = f'https://api.hamsterkombat.io{endpoint}'
        else:
            return None, "URL or endpoint must be provided"
        
        attempt = 0
        while attempt < retries:
            try:
                async with aiohttp.ClientSession(headers=temp_header) as session:
                    if method.upper() == 'GET':
                        async with session.get(endpoint, params=data, timeout=timeout) as response:
                            if response.status != 422:
                                response.raise_for_status()
                            try:
                                return await response.json(), None
                            except aiohttp.ContentTypeError:
                                return json.loads(await response.text()), None
                    elif method.upper() == 'POST':
                        async with session.post(endpoint, json=data, timeout=timeout) as response:
                            if response.status != 422:
                                response.raise_for_status()
                            try:
                                return await response.json(), None
                            except aiohttp.ContentTypeError:
                                return json.loads(await response.text()), None
                    else:
                        return None, f"Unsupported HTTP method: {method}"
            except (aiohttp.ClientError, asyncio.TimeoutError, requests.exceptions.HTTPError) as e:
                attempt += 1
                if attempt == retries:
                    return None, str(e)
                
                wait_time = backoff_factor * (2 ** (attempt - 1))
                logger.error(f"{self.session} | attempt <y>{attempt}</y>, <r>{wait_time} sec</r> before retry!")
                await asyncio.sleep(wait_time)

        return None, "Failed after retries"
        
    async def connect_client(self):
        try:
            if not self.client.is_connected():
                await self.client.connect()
                logger.info(f"Connected client: {self.session}")
        except Exception as error:
            logger.info(f"Error connection client: {self.session}, {str(error)}")
            raise InvalidSession(self.session)

    async def disconnect_client(self):
        try:
            if self.client.is_connected():
                await self.client.disconnect()
                logger.info(f"Disconnected client: {self.session}")
        except Exception as error:
            logger.info(f"Error disconnect client: {self.session}, {str(error)}")
            raise Exception(self.session)
        
    async def join_channel(self, channel:str):
        result = False
        try:
            await self.connect_client()
            await self.client(functions.channels.JoinChannelRequest(channel))
            await self.disconnect_client()
            result = True
        except Exception as error:
            logger.error(f"{self.session} | Unknown error during join: {error}")
        
        return result
    
    async def get_web_data(self, only_url: bool = False) -> str:
        try:
            await self.connect_client()

            web_view = await self.client(
                functions.messages.RequestWebViewRequest(
                    peer          = 'hAmster_kombat_bot',
                    bot           = 'hAmster_kombat_bot',
                    platform      = 'android',
                    from_bot_menu = False,
                    start_param   = f'kentId{settings.ADMIN_ID}',
                    url           = 'https://hamsterkombat.io/'
                )
            )

            await self.disconnect_client()

            auth_url    = web_view.url
            tg_web_data = unquote(
                string  = unquote(
                    string = auth_url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0]))
            
            if only_url:
                return auth_url
            
            return tg_web_data
        
        except Exception as error:
            logger.error(f"{self.session} | Failed [webData]: {error}")
            await asyncio.sleep(delay=3)

    async def login(self, tg_web_data: str):
        response, error = await self.send_request(
            method   = 'POST',
            endpoint = '/auth/auth-by-telegram-webapp',
            data     = {
                'initDataRaw' : tg_web_data,
                'fingerprint' : FINGERPRINT
            }
        )

        if response and 'authToken' in response:
            self.token       = response['authToken']
            self.expire_date = datetime.now() + timedelta(minutes=60)

            return self.token
        else:
            logger.error(
                f"{self.session} | Failed [AuthToken]: {error or response}"
            )
            return False
        
    async def get_me_telegram(self):
        response, error = await self.send_request(
            method   = 'POST',
            endpoint = '/auth/me-telegram',
            data     = {}
        )

        if response and 'telegramUser' in response:
            return response['telegramUser']
        else:
            logger.error(
                f"{self.session} | Failed [telegramUser]: {error or response}"
            )
            return False
        
    async def get_profile_data(self):
        response, error = await self.send_request(
            method   = 'POST',
            endpoint = '/clicker/sync',
            data     = {}
        )

        if response:
            return response.get('clickerUser') or response.get('found', {}).get('clickerUser', {})
        else:
            logger.error(
                f"{self.session} | Failed [getProfileData]: {error or response}"
            )
            return False
        
    async def get_config(self):
        response, error = await self.send_request(
            method   = 'POST',
            endpoint = '/clicker/config',
            data     = {}
        )

        if response:
            return response
        else:
            logger.error(
                f"{self.session} | Failed [getConfig]: {error}"
            )
            return False
        
    async def get_tasks(self):
        response, error = await self.send_request(
            method   = 'POST',
            endpoint = '/clicker/list-tasks',
            data     = {}
        )

        if response and 'tasks' in response:
            return response['tasks']
        else:
            logger.error(
                f"{self.session} | Failed [getTasks]: {error or response}"
            )
            return False
        
    async def select_exchange(self, exchange_id: str):
        response, error = await self.send_request(
            method   = 'POST',
            endpoint = '/clicker/select-exchange',
            data     = {'exchangeId': exchange_id}
        )

        if response:
            return True
        else:
            logger.error(
                f"{self.session} | Failed [selectExchange]: {error or response}"
            )
            return False
        
    async def get_daily(self):
        response, error = await self.send_request(
            method   = 'POST',
            endpoint = '/clicker/check-task',
            data     = {'taskId': "streak_days"}
        )

        if response:
            return True
        else:
            logger.error(
                f"{self.session} | Failed [getDaily]: {error or response}"
            )
            return False
        
    async def apply_boost(self, boost_id: str):
        response, error = await self.send_request(
            method   = 'POST',
            endpoint = '/clicker/buy-boost',
            data     = {
                'timestamp' : time(),
                'boostId'   : boost_id
            }
        )

        if response:
            return True
        else:
            logger.error(
                f"{self.session} | Failed [applyBoost]: {error or response}"
            )
            return False
        
    async def get_upgrades(self):
        response, error = await self.send_request(
            method   = 'POST',
            endpoint = '/clicker/upgrades-for-buy',
            data     = {}
        )

        if response and 'upgradesForBuy' in response:
            return response
        else:
            logger.error(
                f"{self.session} | Failed [getUpgrades]: {error or response}"
            )
            return {}
        
    async def buy_upgrade(self, upgrade_id: str):
        response, error = await self.send_request(
            method   = 'POST',
            endpoint = '/clicker/buy-upgrade',
            data     = {
                'timestamp' : time(),
                'upgradeId' : upgrade_id
            }
        )

        if response:
            return True, response.get('upgradesForBuy') or response.get('found', {}).get('upgradesForBuy', {})
        else:
            logger.error(
                f"{self.session} | Failed [buyUpgrade]: {error or response}"
            )
            return False, {}
        
    async def get_boosts(self):
        response, error = await self.send_request(
            method   = 'POST',
            endpoint = '/clicker/boosts-for-buy',
            data     = {}
        )

        if response and 'boostsForBuy' in response:
            return response['boostsForBuy']
        else:
            logger.error(
                f"{self.session} | Failed [getBoost]: {error or response}"
            )
            return []
        
    async def send_taps(self, available_energy: int, taps: int):
        response, error = await self.send_request(
            method   = 'POST',
            endpoint = '/clicker/tap',
            data     = {
                'availableTaps' : available_energy,
                'count'         : taps,
                'timestamp'     : time()
            }
        )

        if response:
            return response.get('clickerUser') or response.get('found', {}).get('clickerUser', {})
        else:
            logger.error(
                f"{self.session} | Failed [sendTaps]: {error or response}"
            )
            return False
        
    async def claim_daily_cipher(self, cipher: str):
        response, error = await self.send_request(
            method   = 'POST',
            endpoint = '/clicker/claim-daily-cipher',
            data     = {'cipher': cipher}
        )

        if response and 'clickerUser' in response:
            return True
        else:
            logger.error(
                f"{self.session} | Failed [ClaimDailyCipher]: {error or response}"
            )
            return False
    
    async def get_nuxt_builds(self):
        response, error = await self.send_request(
            method = 'GET',
            url    = 'https://hamsterkombat.io/_nuxt/builds/meta/32ddd2fc-00f7-4814-bc32-8f160963692c.json',
        )

        if response:
            return True
        else:
            logger.error(
                f"{self.session} | Failed [getNuxtBuilds]: {error or response}"
            )
            return False
    
    async def get_combo_cards(self):
        response, error = await self.send_request(
            method = 'GET',
            url    = 'https://api21.datavibe.top/api/GetCombo'
        )

        if response:
            return response
        else:
            logger.error(
                f"{self.session} | Failed [getComboCards]: {error or response}"
            )
            return False
    
    async def claim_daily_combo(self):
        response, error = await self.send_request(
            method   = 'POST',
            endpoint = '/clicker/claim-daily-combo',
            data     = {}
        )

        if response:
            return True
        else:
            logger.error(
                f"{self.session} | Failed [claimDailyCombo]: {error or response}"
            )
            return False
    
    async def run(self):
        tg_web_data = await self.get_web_data()

        while True:
            try:
                if datetime.now() > self.expire_date:
                    await self.get_nuxt_builds()

                    access_token = await self.login(tg_web_data=tg_web_data)

                    if not access_token:
                        await asyncio.sleep(delay=60)
                        continue

                    self.token       = access_token
                    self.expire_date = datetime.now() + timedelta(minutes=60)
                    self.update_headers({'Authorization' : f"Bearer {access_token}"})

                    logger.info(f"{self.session} | <m>Auth reloaded!</m>")

                    await self.get_me_telegram()

                    game_config  = await self.get_config()
                    profile_data = await self.get_profile_data()

                    if not profile_data:
                        continue

                    balance           = int(profile_data.get('balanceCoins', 0))
                    last_passive_earn = int(profile_data.get('lastPassiveEarn', 0))
                    earn_on_hour      = int(profile_data.get('earnPassivePerHour', 0))

                    logger.info(
                        f"{self.session} | Last passive earn: <g>+{last_passive_earn:,}</g> | "
                        f"Earn every hour: <y>{earn_on_hour:,}</y>"
                    )

                    upgrades_data = await self.get_upgrades()

                    if upgrades_data:
                        upgrades    = upgrades_data['upgradesForBuy']
                        daily_combo = upgrades_data.get('dailyCombo', 0)

                        if daily_combo:
                            bonus      = daily_combo['bonusCoins']
                            is_claimed = daily_combo['isClaimed']

                            if not is_claimed:
                                combo_cards = await self.get_combo_cards()
                                cards       = combo_cards['combo']
                                date        = combo_cards['date']

                                available_combo_cards = [
                                    data for data in upgrades
                                    if data['isAvailable'] is True
                                    and data['id'] in cards
                                    and data['id'] not in daily_combo['upgradeIds']
                                    and data['isExpired'] is False
                                    and data.get('cooldownSeconds', 0) == 0
                                    and data.get('maxLevel', data['level']) >= data['level']
                                    and (data.get('condition') is None
                                            or data['condition'].get('_type') != 'SubscribeTelegramChannel')
                                ]

                                if date == datetime.now().strftime("%d-%m-%y"):
                                    common_price = sum([upgrade['price'] for upgrade in available_combo_cards])

                                    logger.info(
                                        f"{self.session} | "
                                        f"Found <m>{len(available_combo_cards)}</m> combo cards to get!"
                                    )

                                    if common_price < bonus and balance > common_price:
                                        for upgrade in available_combo_cards:
                                            upgrade_id = upgrade['id']
                                            level      = upgrade['level']
                                            price      = upgrade['price']
                                            profit     = upgrade['profitPerHourDelta']

                                            logger.info(
                                                f"{self.session} | "
                                                f"Sleep 5s before upgrade <r>combo</r> card <e>{upgrade_id}</e>"
                                            )

                                            await asyncio.sleep(delay=5)

                                            status, upgrades = await self.buy_upgrade(
                                                upgrade_id   = upgrade_id
                                            )

                                            if status is True:
                                                earn_on_hour += profit
                                                balance      -= price

                                                logger.success(
                                                    f"{self.session} | "
                                                    f"Successfully upgraded <e>{upgrade_id}</e> with price <r>{price:,}</r> to <m>{level}</m> lvl | "
                                                    f"Earn every hour: <y>{earn_on_hour:,}</y> (<g>+{profit:,}</g>) | "
                                                    f"Money left: <e>{balance:,}</e>"
                                                )
                                                await asyncio.sleep(delay=1)

                                        await asyncio.sleep(delay=2)

                                        status = await self.claim_daily_combo()

                                        if status is True:
                                            logger.success(
                                                f"{self.session} | Successfully claimed daily combo | "
                                                f"Bonus: <g>+{bonus:,}</g>"
                                            )


                    tasks        = await self.get_tasks()
                    daily_task   = tasks[-1]
                    rewards      = daily_task['rewardsByDays']
                    is_completed = daily_task['isCompleted']
                    days         = daily_task['days']
                    daily_cipher = game_config.get('dailyCipher', False)

                    await asyncio.sleep(delay=2)

                    if is_completed is False:
                        status = await self.get_daily()
                        if status is True:
                            logger.success(
                                f"{self.session} | Successfully get daily reward | "
                                f"Days: <m>{days}</m> | Reward coins: {rewards[days - 1]['rewardCoins']}"
                            )

                    await asyncio.sleep(delay=2)
                    
                    if daily_cipher:
                        cipher     = daily_cipher['cipher']
                        bonus      = daily_cipher['bonusCoins']
                        is_claimed = daily_cipher['isClaimed']

                        if not is_claimed and cipher:
                            decoded_cipher = decode_cipher(cipher=cipher)
                            status         = await self.claim_daily_cipher(cipher=decoded_cipher)

                            if status is True:
                                logger.success(
                                    f"{self.session} | "
                                    f"Successfully claim daily cipher: <y>{decoded_cipher}</y> | "
                                    f"Bonus: <g>+{bonus:,}</g>"
                                )
                        
                        await asyncio.sleep(delay=2)
                    
                    exchange_id = profile_data.get('exchangeId')
                    if not exchange_id:
                        status = await self.select_exchange(exchange_id="bybit")
                        if status is True:
                            logger.success(f"{self.session} | Successfully selected exchange <y>Bybit</y>")

                
                logger.info(f"{self.session} | account fully loaded! | <m>start working...</m>")
                taps = randint(a=settings.RANDOM_TAPS_COUNT[0], b=settings.RANDOM_TAPS_COUNT[1])

                profile_data = await self.get_profile_data()
                
                if profile_data:
                    available_energy = profile_data.get('availableTaps', 0)
                else:
                    available_energy = 100

                player_data = await self.send_taps(
                    available_energy = available_energy,
                    taps             = taps
                )

                if not player_data:
                    continue

                available_energy = player_data.get('availableTaps', 0)
                new_balance      = int(player_data.get('balanceCoins', 0))
                calc_taps        = abs(new_balance - balance) if 'balance' in locals() else 0
                balance          = new_balance
                total            = int(player_data.get('totalCoins', 0))
                earn_on_hour     = int(player_data.get('earnPassivePerHour', 0))

                logger.success(
                    f"{self.session} | Successful tapped! | "
                    f"Balance: <c>{balance:,}</c> (<g>+{calc_taps:,}</g>) | Total: <e>{total:,}</e>"
                )

                if settings.AUTO_UPGRADE is True:
                    upgrades = await self.get_upgrades()
                    for _ in range(settings.UPGRADES_COUNT):
                        if isinstance(upgrades, dict):
                            upgrades = upgrades.get('upgradesForBuy', [])
                        elif isinstance(upgrades, list):
                            pass
                        else:
                            upgrades = []
                        
                        available_upgrades = [
                            data for data in upgrades
                            if data['isAvailable'] is True
                                and data['isExpired'] is False
                                and data.get('cooldownSeconds', 0) == 0
                                and data.get('maxLevel', data['level']) >= data['level']
                            and (
                                data.get('condition') is None
                                or data['condition'].get('_type') != 'SubscribeTelegramChannel'
                            )
                        ]

                        free_money = balance - settings.BALANCE_TO_SAVE
                        queue      = find_best(free_money, available_upgrades)

                        if not queue:
                            continue
                        
                        upgrade    = queue[0]
                        upgrade_id = upgrade['id']
                        level      = upgrade['level']
                        price      = upgrade['price']
                        profit     = upgrade['profit']

                        logger.info(f"{self.session} | Sleep 5s before upgrade <e>{upgrade_id}</e>")
                        await asyncio.sleep(delay=5)

                        status, upgrades = await self.buy_upgrade(
                            upgrade_id   = upgrade_id
                        )

                        if status is True:
                            earn_on_hour += profit
                            balance      -= price

                            logger.success(
                                f"{self.session} | "
                                f"Successfully upgraded <e>{upgrade_id}</e> with price <r>{price:,}</r> to <m>{level}</m> lvl | "
                                f"Earn every hour: <y>{earn_on_hour:,}</y> (<g>+{profit:,}</g>) | "
                                f"Money left: <e>{balance:,}</e>"
                            )

                            await asyncio.sleep(delay=1)
                            continue
                
                if available_energy < settings.MIN_AVAILABLE_ENERGY:
                    boosts       = await self.get_boosts()
                    energy_boost = next((boost for boost in boosts if boost['id'] == 'BoostFullAvailableTaps'), {})

                    if (
                        settings.APPLY_DAILY_ENERGY is True
                        and energy_boost.get("cooldownSeconds", 0) == 0
                        and energy_boost.get("level", 0) <= energy_boost.get("maxLevel", 0)
                    ):
                        logger.info(f"{self.session} | Sleep 5s before apply energy boost")
                        await asyncio.sleep(delay=5)

                        status = await self.apply_boost(boost_id="BoostFullAvailableTaps")

                        if status is True:
                            logger.success(f"{self.session} | Successfully apply energy boost")
                            await asyncio.sleep(delay=1)
                            continue

                    random_sleep = randint(settings.SLEEP_BY_MIN_ENERGY[0], settings.SLEEP_BY_MIN_ENERGY[1])

                    logger.info(f"{self.session} | Minimum energy reached: {available_energy}")
                    logger.info(f"{self.session} | Sleep {random_sleep:,}s")

                    await asyncio.sleep(delay=random_sleep)
                    #self.expire_date = datetime.now()

            except Exception as error:
                print(traceback.format_exc())
                logger.error(f"{self.session} | Unknown error: {error}")
                await asyncio.sleep(delay=3)

            else:
                sleep_clicks = randint(a=settings.SLEEP_BETWEEN_TAP[0], b=settings.SLEEP_BETWEEN_TAP[1])
                logger.info(f"{self.session} | sleep clicks {sleep_clicks}s")
                await asyncio.sleep(delay=sleep_clicks)