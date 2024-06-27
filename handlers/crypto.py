import os

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from services.crypto_data import get_crypto_data
from services.signals import generate_signals
from services.charts import create_chart


async def send_top_cryptos(message: types.Message):
    data = get_crypto_data()
    buttons = [
        InlineKeyboardButton(text=f"{coin['name']}: {coin['current_price']} USD", callback_data=f"chart_{coin['id']}")
        for coin in data
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    await message.reply("Выберите криптовалюту для просмотра графика:", reply_markup=keyboard)


async def send_signals(message: types.Message):
    data = get_crypto_data()
    signals = generate_signals(data)
    response = "\n".join(signals) if signals else "Нет сигналов."
    await message.reply(response)


async def send_chart_prompt(message: types.Message):
    await message.reply("Выберите криптовалюту из списка Топ 10 криптовалют.")


async def send_chart(callback_query: types.CallbackQuery):
    coin_name = callback_query.data.split("_")[1]  # Используем data вместо text
    data = get_crypto_data()
    if data:
        create_chart(data, coin_name)
        photo_path = f'{coin_name}.png'
        if os.path.exists(photo_path):
            with open(photo_path, 'rb') as photo:
                await callback_query.message.answer_photo(InputFile(photo), caption=f'График цены {coin_name}')
        else:
            await callback_query.message.reply("Не удалось создать график. Попробуйте позже.")
    else:
        await callback_query.message.reply("Не удалось получить данные о криптовалютах. Попробуйте позже.")


def register_handlers_crypto(dp: Dispatcher):
    dp.message.register(send_top_cryptos, lambda message: message.text == 'Топ 10 криптовалют')
    dp.message.register(send_signals, lambda message: message.text == 'Сигналы на покупку/продажу')
    dp.message.register(send_chart_prompt, lambda message: message.text == 'График криптовалюты')
    dp.callback_query.register(send_chart, lambda call: call.data.startswith('chart_'))
