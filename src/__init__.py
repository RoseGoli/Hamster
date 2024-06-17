import os
from src.config import settings

if not os.path.exists(settings.SESSION_PATH):
    os.mkdir(settings.SESSION_PATH)

if not os.path.exists(settings.BAD_SESSIONS_PATH):
    os.mkdir(settings.BAD_SESSIONS_PATH)