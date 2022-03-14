from aiogram import Dispatcher, Bot
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

from data import config

webhook_path = f'/bot/{config.BOT_TOKEN}'
webhook_host = 'https://4ecb-91-202-130-51.ngrok.io'
WEBHOOK_URL = f"{webhook_host}{webhook_path}"


async def on_startup(dispatcher: Dispatcher):
    import middlewares
    from database.db_api import create_db
    import handlers
    create_db()
    middlewares.setup(dp)
    handlers.setup(dp)


if __name__ == '__main__':
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML, validate_token=True)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    executor.start_polling(dispatcher=dp, on_startup=on_startup, skip_updates=True)
