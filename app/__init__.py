from flask import Flask
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Инициализация расширений вне функции create_app
cache = Cache()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

def create_app():
    app = Flask(__name__)
    
    # Конфигурация
    app.config.from_mapping(
        CACHE_TYPE='SimpleCache',
        CACHE_DEFAULT_TIMEOUT=300,
        RATE_LIMIT_DEFAULT="100 per minute",
        SECRET_KEY='your-secret-key-here',
        CBR_URL='https://www.cbr.ru/scripts/XML_daily.asp',
        USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    
    # Инициализация расширений с приложением
    cache.init_app(app)
    limiter.init_app(app)
    
    # Регистрация маршрутов
    from .routes import init_routes
    init_routes(app, limiter)
    
    # Регистрация обработчиков ошибок
    from .errors import handle_404, handle_500
    app.register_error_handler(404, handle_404)
    app.register_error_handler(500, handle_500)
    
    # Добавляем cache в app для удобного доступа
    app.cache = cache
    
    return app