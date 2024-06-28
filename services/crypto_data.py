import logging
import aiohttp
import asyncio

import requests
from aiocache import Cache
from config import CRYPTO_API_URL, CRYPTO_API_PARAMS, CHECK_INTERVAL, CRYPTO_HISTORY_API_URL

logger = logging.getLogger(__name__)

# Настройка кеша
cache = Cache(Cache.MEMORY, ttl=60*60)  # Время жизни кеша 60 секунд

# Настройка семафора для троттлинга
semaphore = asyncio.Semaphore(30)  # Максимум 30 запросов в минуту


def get_crypto_data():
    response = requests.get(CRYPTO_API_URL, params=CRYPTO_API_PARAMS)
    return response.json()


async def get_crypto_history_data(coin_id, days=7):
    cache_key = f"{coin_id}_{days}"
    # Проверка наличия данных в кеше
    cached_data = await cache.get(cache_key)
    if cached_data:
        return cached_data

    url = CRYPTO_HISTORY_API_URL.format(id=coin_id)
    params = {
        'vs_currency': 'usd',
        'days': days,
    }

    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()
                # Сохранение данных в кеше
                await cache.set(cache_key, data.get('prices', []))
                return data.get('prices', [])
