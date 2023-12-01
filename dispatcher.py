from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
bot = Bot(token='6984183757:AAHw9F58Wg9fEK2Zjk6rwqqqZmrUB_zRZfU')
dp = Dispatcher(bot, storage=MemoryStorage())
