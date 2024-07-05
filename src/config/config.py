from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID              : int
    API_HASH            : str
    TG_TOKEN            : str
    OWNERS              : list[int]
    
    MAIN_NAME           : str = 'bot'
    SESSION_PATH        : str = 'sessions'
    BAD_SESSIONS_PATH   : str = 'bad_sessions'

    MIN_AVAILABLE_ENERGY: int = 100
    SLEEP_BY_MIN_ENERGY : list[int] = [1800, 2400]

    MAX_LEVEL           : int  = 20
    BALANCE_TO_SAVE     : int = 1000000
    UPGRADES_COUNT      : int = 10

    RANDOM_TAPS_COUNT   : list[int] = [10, 50]
    SLEEP_BETWEEN_TAP   : list[int] = [10, 25]
    RENEW_AUTH          : int = 3600

settings = Settings()