import json
import aiohttp
import asyncio

from .logger import logger

class Request:
    def __init__(self, base_url=None, base_headers=None):
        self.base_url     = base_url
        self.base_headers = base_headers if base_headers is not None else {}
        self.headers      = {}

    def set_header(self, key, value):
        self.headers[key] = value

    def update_headers(self, new_headers):
        self.headers.update(new_headers)

    async def send_request(self, method, url=None, endpoint=None, data=None, timeout=15, retries=3, backoff_factor=1):
        combined_headers = {**self.base_headers, **self.headers}

        if not (url or endpoint):
            return None, "URL or endpoint must be provided"

        if endpoint and self.base_url:
            url = f'{self.base_url}{endpoint}'
        
        elif endpoint:
            return None, "Base URL must be provided if using endpoint"
        
        elif url:
            url = url

        attempt = 0

        while attempt < retries:
            try:
                async with aiohttp.ClientSession(headers=combined_headers) as session:
                    if method.upper() == 'GET':
                        async with session.get(url, params=data, timeout=timeout) as response:
                            return await self._handle_response(response)
                    elif method.upper() == 'POST':
                        async with session.post(url, json=data, timeout=timeout) as response:
                            return await self._handle_response(response)
                    else:
                        return None, f"Unsupported HTTP method: {method}"
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                attempt += 1
                if attempt == retries:
                    return None, str(e)

                wait_time = backoff_factor * (2 ** (attempt - 1))
                logger.error(f"Attempt {attempt}, waiting {wait_time} seconds before retry!")
                await asyncio.sleep(wait_time)

        return None, "Failed after retries"

    async def _handle_response(self, response, ignore_status :list = [422]):
        try:
            if response.status not in ignore_status:
                response.raise_for_status()
            try:
                return await response.json(), None
            except aiohttp.ContentTypeError:
                return json.loads(await response.text()), None
        except aiohttp.ClientResponseError as e:
            return None, str(e)