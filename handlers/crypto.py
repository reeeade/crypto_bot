from aiogram import types, Bot, Dispatcher
import logging
from config import API_TOKEN
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from services.crypto_data import get_crypto_data, get_crypto_history_data
from services.charts import create_chart
from services.signals import generate_signals

logger = logging.getLogger(__name__)
bot = Bot(token=API_TOKEN)


async def send_top_cryptos(message: types.Message):
    data = get_crypto_data()
    response = "Топ 10 криптовалют:\n"
    for coin in data:
        response += f"{coin['name']} (Цена: {coin['current_price']} USD)\n"
    await message.answer(response)


async def send_signals(message: types.Message):
    try:
        data = get_crypto_data()
        signals = await generate_signals(data)

        if signals:
            await message.answer("\n".join(signals))
        else:
            await message.answer("Сигналы не найдены.")
    except Exception as e:
        logger.error(f"An error occurred while generating signals: {e}")
        await message.answer("Не удалось получить сигналы. Попробуйте позже.")


async def send_chart_prompt(message: types.Message):
    data = get_crypto_data()
    buttons = [
        types.InlineKeyboardButton(text=f"{coin['name']}: {coin['current_price']} USD",
                                   callback_data=f"chart_{coin['id']}")
        for coin in data
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 2] for i in range(0, len(buttons), 2)])

    await message.answer("Выберите криптовалюту для просмотра графика:", reply_markup=keyboard)


async def send_chart(callback_query: types.CallbackQuery, state: FSMContext):
    coin_id = callback_query.data.split('_', 1)[1].lower()
    prices = await get_crypto_history_data(coin_id)
    try:
        photo_path = create_chart(prices, coin_id)
        photo = FSInputFile(photo_path)

        # Получение данных из состояния
        data = await state.get_data()
        last_chart_msg_id = data.get('last_chart_msg_id')

        # Замена предыдущего графика, если он существует
        if last_chart_msg_id:
            try:
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=last_chart_msg_id)
            except Exception as e:
                logger.error(f"An error occurred while updating the chart: {e}")
                await callback_query.message.answer("Не удалось обновить график. Попробуйте позже.")
            # Отправка нового графика и сохранение идентификатора сообщения
        msg = await callback_query.message.answer_photo(photo, caption=f"График цены {coin_id}")
        await state.update_data(last_chart_msg_id=msg.message_id)
    except Exception as e:
        logger.error(f"An error occurred while creating the chart: {e}")
        await callback_query.message.answer("Не удалось создать график. Попробуйте позже.")


def register_handlers_crypto(dp: Dispatcher):
    dp.message.register(send_top_cryptos, lambda message: message.text == 'Топ 10 криптовалют')
    dp.message.register(send_signals, lambda message: message.text == 'Сигналы на покупку/продажу')
    dp.message.register(send_chart_prompt, lambda message: message.text == 'График криптовалюты')
    dp.callback_query.register(send_chart, lambda call: call.data.startswith('chart_'))
