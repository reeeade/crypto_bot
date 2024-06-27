import logging
import requests
import asyncio
from config import CRYPTO_API_URL, CRYPTO_API_PARAMS, CHECK_INTERVAL
from services.signals import generate_signals
from aiogram import Bot, Dispatcher


def get_crypto_data():
    try:
        response = requests.get(CRYPTO_API_URL, params=CRYPTO_API_PARAMS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")


async def monitor_market(bot: Bot, dp: Dispatcher):
    while True:
        # Используем правильный метод для получения текущего состояния
        state = dp.fsm.current_state()
        data = await state.get_data()

        if data.get('monitoring'):
            crypto_data = get_crypto_data()
            signals = generate_signals(crypto_data)
            if signals:
                message = "\n".join(signals)
                user_id = data.get('user_id')
                if user_id:
                    await bot.send_message(chat_id=user_id, text=message)

        await asyncio.sleep(CHECK_INTERVAL)
