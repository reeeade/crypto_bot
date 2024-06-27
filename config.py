import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
CRYPTO_API_URL = 'https://api.coingecko.com/api/v3/coins/markets'
CRYPTO_API_PARAMS = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 10,
    'page': 1,
    'sparkline': True  # Включаем исторические данные для анализа
}
CHECK_INTERVAL = 60  # Интервал проверки данных - 1 минута
SMA_SHORT_WINDOW = 14  # Короткий период скользящей средней
SMA_LONG_WINDOW = 50  # Длинный период скользящей средней
RSI_PERIOD = 14  # Период для RSI
ADX_PERIOD = 14  # Период для ADX
BUY_THRESHOLD_RSI = 30  # Порог для RSI при покупке
SELL_THRESHOLD_RSI = 70  # Порог для RSI при продаже
BUY_THRESHOLD_ADX = 25  # Порог для ADX при покупке
