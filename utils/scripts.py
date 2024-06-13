import random
import string
import base64
import hashlib

from urllib.parse import unquote
from fake_useragent import UserAgent

def generate_random_visitor_id():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    visitor_id    = hashlib.md5(random_string.encode()).hexdigest()

    return visitor_id

def escape_html(text: str) -> str:
    return text.replace('<', '\\<').replace('>', '\\>')

def decode_cipher(cipher: str) -> str:
    encoded = cipher[:3] + cipher[4:]
    return base64.b64decode(encoded).decode('utf-8')

def find_best(balance, upgrades, old=None):
    if old is None:
        old = []
    
    if not upgrades:
        return old

    max_upgrade     = {'index': 0}
    max_upgrade_key = None

    for key, upgrade in enumerate(upgrades):
        if (
            not upgrade['isAvailable'] or
            upgrade['isExpired'] or
            balance < upgrade['price']
        ):
            continue

        index = upgrade['profitPerHourDelta'] / upgrade['price']

        if index > max_upgrade['index']:
            max_upgrade_key = key
            max_upgrade     = {
                'id'     : upgrade['id'],
                'key'    : key,
                'price'  : upgrade['price'],
                'index'  : index,
                'profit' : upgrade['profitPerHourDelta'],
                'level'  : upgrade['level']
            }
    
    if max_upgrade['index'] == 0:
        return old

    new_upgrades = [upgrade for i, upgrade in enumerate(upgrades) if i != max_upgrade_key]
    return find_best(balance - max_upgrade['price'], new_upgrades, old + [max_upgrade])

def get_mobile_user_agent() -> str:
    """
    Function: get_mobile_user_agent

    This method generates a random mobile user agent for an Android platform.
    If the generated user agent does not contain the "wv" string,
    it adds it to the browser version component.

    :return: A random mobile user agent for Android platform.
    """
    ua = UserAgent(platforms=['mobile'], os=['android'])
    user_agent = ua.random
    if 'wv' not in user_agent:
        parts = user_agent.split(')')
        parts[0] += '; wv'
        user_agent = ')'.join(parts)
    return user_agent

def parse_webapp_url(auth_url: str) -> str:
    return unquote(
        string = unquote(
            string = auth_url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0]))