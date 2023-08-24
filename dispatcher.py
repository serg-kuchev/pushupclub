from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
bot = Bot(token='6200017899:AAFxYqe2-BiBU_k0HsZLnGTWZ-pYBMbGeUQ')
dp = Dispatcher(bot, storage=MemoryStorage())