from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

menu_button = KeyboardButton(text='/menu')
menu_markup = ReplyKeyboardMarkup(keyboard=[[menu_button]], resize_keyboard=True)


async def show_menu(message: types.Message):
    buttons = [
        KeyboardButton(text='Топ 10 криптовалют'),
        KeyboardButton(text='График криптовалюты'),
        KeyboardButton(text='Сигналы на покупку/продажу'),
        KeyboardButton(text='Мониторинг')
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)
    await message.reply("Выберите опцию:", reply_markup=keyboard)


async def show_monitoring_menu(message: types.Message):
    buttons = [
        InlineKeyboardButton(text="Запустить мониторинг", callback_data='start_monitoring'),
        InlineKeyboardButton(text="Остановить мониторинг", callback_data='stop_monitoring')
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    await message.reply("Управление мониторингом:", reply_markup=keyboard)


def register_handlers_menu(dp: Dispatcher):
    dp.message.register(show_menu, lambda message: message.text == '/menu')
    dp.message.register(show_monitoring_menu, lambda message: message.text == 'Мониторинг')
