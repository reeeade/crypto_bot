from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


async def start_monitoring(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(monitoring=True)
    await callback_query.answer("Мониторинг запущен.")
    await callback_query.message.edit_text("Мониторинг запущен.")


async def stop_monitoring(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(monitoring=False)
    await callback_query.answer("Мониторинг остановлен.")
    await callback_query.message.edit_text("Мониторинг остановлен.")


def register_handlers_monitoring(dp: Dispatcher):
    dp.callback_query.register(start_monitoring, lambda call: call.data == 'start_monitoring')
    dp.callback_query.register(stop_monitoring, lambda call: call.data == 'stop_monitoring')
