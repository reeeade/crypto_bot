from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command


class UserState(StatesGroup):
    user_id = State()
    monitoring = State()


async def send_welcome(message: types.Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await state.update_data(monitoring=False)
    await message.reply("Привет! Я бот для отслеживания криптовалют. Используй /menu для навигации.")


def register_handlers_start(dp: Dispatcher):
    dp.message.register(send_welcome, Command(commands=['start', 'help']))
