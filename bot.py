from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from config import API_TOKEN
from handlers import start, menu, crypto, monitoring
from services.crypto_data import monitor_market
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация обработчиков
start.register_handlers_start(dp)
menu.register_handlers_menu(dp)
crypto.register_handlers_crypto(dp)
monitoring.register_handlers_monitoring(dp)


# Асинхронная функция для запуска мониторинга
async def on_startup(dispatcher):
    await bot.set_my_commands([BotCommand(command="/start", description="Запустить бота")])
    await monitor_market(bot, dp)


# Запуск бота
if __name__ == '__main__':
    dp.run_polling(bot, on_startup=on_startup)
