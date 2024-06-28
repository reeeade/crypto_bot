import pandas as pd
import pandas_ta as ta
import logging
from config import SMA_SHORT_WINDOW, SMA_LONG_WINDOW, RSI_PERIOD, ADX_PERIOD, BUY_THRESHOLD_RSI, SELL_THRESHOLD_RSI, \
    BUY_THRESHOLD_ADX
from services.crypto_data import get_crypto_history_data

logger = logging.getLogger(__name__)


def calculate_indicators(df):
    df['SMA_SHORT'] = ta.sma(df['price'], length=SMA_SHORT_WINDOW)
    df['SMA_LONG'] = ta.sma(df['price'], length=SMA_LONG_WINDOW)
    df['RSI'] = ta.rsi(df['price'], length=RSI_PERIOD)
    adx = ta.adx(df['price'], df['price'], df['price'], length=ADX_PERIOD)
    df['ADX'] = adx['ADX_14'] if 'ADX_14' in adx else None
    return df


async def generate_signals(data):
    signals = []
    for coin in data:
        if 'id' in coin:
            coin_id = coin['id']
            try:
                prices = await get_crypto_history_data(coin_id)
                if not prices:
                    logger.warning(f"Не удалось получить данные истории для {coin_id}")
                    continue

                df = pd.DataFrame(prices, columns=['timestamp', 'price'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df.set_index('timestamp', inplace=True)
                df = calculate_indicators(df)
                latest = df.iloc[-1]

                logger.info(
                    f"{coin['name']} - Latest Indicators: SMA_SHORT: {latest['SMA_SHORT']}, SMA_LONG: {latest['SMA_LONG']}, RSI: {latest['RSI']}, ADX: {latest['ADX']}")

                if pd.notna(latest['SMA_SHORT']) and pd.notna(latest['SMA_LONG']) and pd.notna(
                        latest['RSI']) and pd.notna(latest['ADX']):
                    if (latest['SMA_SHORT'] > latest['SMA_LONG'] and latest['RSI'] < BUY_THRESHOLD_RSI and latest[
                        'ADX'] > BUY_THRESHOLD_ADX):
                        signals.append(f"Покупка: {coin['name']} ({coin['current_price']} USD)")
                        logger.info(f"Покупка сигнал добавлен для {coin['name']}")
                    elif latest['SMA_SHORT'] < latest['SMA_LONG'] and latest['RSI'] > SELL_THRESHOLD_RSI:
                        signals.append(f"Продажа: {coin['name']} ({coin['current_price']} USD)")
                        logger.info(f"Продажа сигнал добавлен для {coin['name']}")
                else:
                    logger.warning(f"Не удалось получить индикаторы для {coin['name']}")

                if latest.isnull().any():
                    logger.warning(f"Индикаторы для {coin['name']} содержат None значения: {latest.to_dict()}")

            except Exception as e:
                logger.error(f"Ошибка при обработке данных для {coin_id}: {e}")

        else:
            logger.warning(f"Монета не содержит 'id': {coin}")
    return signals
