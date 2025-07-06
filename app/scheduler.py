from flask_apscheduler import APScheduler
from .utils import get_currency_rates
import logging

scheduler = APScheduler()
logger = logging.getLogger('currency_app')

def update_currency_rates(app):
    with app.app_context():
        logger.info("Scheduled currency update started")
        # Принудительное обновление кэша
        rates = get_currency_rates()
        logger.info(f"Updated rates for {len(rates)} currencies")

def init_scheduler(app):
    if app.config.get('SCHEDULER_ENABLE', False):
        scheduler.init_app(app)
        
        # Задача обновления каждые 6 часов
        scheduler.add_job(
            id='update_currency_rates',
            func=update_currency_rates,
            args=[app],
            trigger='interval',
            hours=6
        )
        
        scheduler.start()
        logger.info("Scheduler started")