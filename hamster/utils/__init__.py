import os

from .logger import logger
from . import launcher
from ...utils import scripts
from . import fingerprint

if not os.path.exists(path='sessions'):
    os.mkdir(path='sessions')