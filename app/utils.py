import logging
import requests
from datetime import datetime
from flask import current_app
import xml.etree.ElementTree as ET

logger = logging.getLogger('currency_app')

CURRENCY_FLAGS = {
    'AUD': '/static/flags/au.svg',
    'AZN': '/static/flags/az.svg',
    'GBP': '/static/flags/gb.svg',
    'AMD': '/static/flags/am.svg',
    'BYN': '/static/flags/by.svg',
    'BGN': '/static/flags/bg.svg',
    'BRL': '/static/flags/br.svg',
    'HUF': '/static/flags/hu.svg',
    'HKD': '/static/flags/hk.svg',
    'DKK': '/static/flags/dk.svg',
    'USD': '/static/flags/us.svg',
    'EUR': '/static/flags/eu.svg',
    'INR': '/static/flags/in.svg',
    'KZT': '/static/flags/kz.svg',
    'CAD': '/static/flags/ca.svg',
    'KGS': '/static/flags/kg.svg',
    'CNY': '/static/flags/cn.svg',
    'MDL': '/static/flags/md.svg',
    'NOK': '/static/flags/no.svg',
    'PLN': '/static/flags/pl.svg',
    'RON': '/static/flags/ro.svg',
    'RUB': '/static/flags/ru.svg',
    'SGD': '/static/flags/sg.svg',
    'TJS': '/static/flags/tj.svg',
    'TRY': '/static/flags/tr.svg',
    'TMT': '/static/flags/tm.svg',
    'UZS': '/static/flags/uz.svg',
    'UAH': '/static/flags/ua.svg',
    'CZK': '/static/flags/cz.svg',
    'SEK': '/static/flags/se.svg',
    'CHF': '/static/flags/ch.svg',
    'KRW': '/static/flags/kr.svg',
    'JPY': '/static/flags/jp.svg',
    'GEL': '/static/flags/ge.svg',
    'DEFAULT': '/static/flags/default.svg'
}

def get_currency_rates():
    """Получает курсы валют с сайта ЦБ РФ"""
    cache = current_app.extensions["cache"][list(current_app.extensions["cache"].keys())[0]]
    cache_key = "currency_rates_cache"
    
    cached_rates = cache.get(cache_key)
    if cached_rates:
        return cached_rates

    try:
        config = current_app.config
        response = requests.get(
            config['CBR_URL'],
            headers={'User-Agent': config['USER_AGENT']},
            timeout=10
        )
        response.raise_for_status()

        root = ET.fromstring(response.content)
        currencies = {
            'RUB': {
                'rate': 1.0,
                'name': 'Российский рубль',
                'unit': 1,
                'flag': CURRENCY_FLAGS['RUB']
            }
        }

        for valute in root.findall('Valute'):
            try:
                code = valute.find('CharCode').text
                name = valute.find('Name').text
                nominal = int(valute.find('Nominal').text)
                value = float(valute.find('Value').text.replace(',', '.'))
                
                currencies[code] = {
                    'rate': value / nominal,
                    'name': name,
                    'unit': nominal,
                    'flag': CURRENCY_FLAGS.get(code, CURRENCY_FLAGS['DEFAULT'])
                }
            except (AttributeError, ValueError) as e:
                logger.error(f"Error parsing currency {code}: {e}")
                continue

        cache.set(cache_key, currencies, timeout=3600)
        return currencies

    except Exception as e:
        logger.error(f"Error fetching rates: {e}")
        return cached_rates or {}

def convert_currency(amount, from_curr, to_curr):
    """Конвертирует валюту"""
    rates = get_currency_rates()
    
    if not rates:
        raise ValueError("Currency rates not available")
    
    if from_curr not in rates:
        raise ValueError(f"Invalid source currency: {from_curr}")
    if to_curr not in rates:
        raise ValueError(f"Invalid target currency: {to_curr}")
    
    rub_amount = amount * rates[from_curr]['rate']
    result = rub_amount / rates[to_curr]['rate']
    
    return round(result, 4)

def setup_logger():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger