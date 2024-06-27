import pandas as pd
import pandas_ta as ta
from config import SMA_SHORT_WINDOW, SMA_LONG_WINDOW, RSI_PERIOD, ADX_PERIOD, BUY_THRESHOLD_RSI, SELL_THRESHOLD_RSI, \
    BUY_THRESHOLD_ADX


def calculate_indicators(df):
    df['SMA_SHORT'] = ta.sma(df['price'], length=SMA_SHORT_WINDOW)
    df['SMA_LONG'] = ta.sma(df['price'], length=SMA_LONG_WINDOW)
    df['RSI'] = ta.rsi(df['price'], length=RSI_PERIOD)
    df['ADX'] = ta.adx(df['price'], df['price'], df['price'], length=ADX_PERIOD)['ADX_14']
    return df


def generate_signals(data):
    signals = []
    for coin in data:
        if 'sparkline_in_7d' in coin:
            prices = pd.Series(coin['sparkline_in_7d']['price'])
            df = pd.DataFrame(prices, columns=['price'])
            df = calculate_indicators(df)
            latest = df.iloc[-1]

            if (latest['SMA_SHORT'] > latest['SMA_LONG'] and latest['RSI'] < BUY_THRESHOLD_RSI and latest['ADX']
                    > BUY_THRESHOLD_ADX):
                signals.append(f"Покупка: {coin['name']} ({coin['current_price']} USD)")
            elif latest['SMA_SHORT'] < latest['SMA_LONG'] and latest['RSI'] > SELL_THRESHOLD_RSI:
                signals.append(f"Продажа: {coin['name']} ({coin['current_price']} USD)")
    return signals
