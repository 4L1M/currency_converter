class Config:
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
    RATE_LIMIT_DEFAULT = "100 per minute"
    SECRET_KEY = 'your-secret-key-here'
    CBR_URL = 'https://www.cbr.ru/scripts/XML_daily.asp'
    USER_AGENT = 'Mozilla/5.0'