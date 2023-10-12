from aiogram import Bot, Dispatcher
from telegram_bot.support_bot.data import TOKEN_API
from aiogram.contrib.fsm_storage.memory import MemoryStorage




storage = MemoryStorage()
bot = Bot(token=TOKEN_API, parse_mode ='HTML')
dp = Dispatcher(bot=bot, storage=storage)


