import asyncio

from aiogram import Bot, Dispatcher

from config import CHECK_INTERVAL
from services.crypto_data import get_crypto_data
from services.signals import generate_signals


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