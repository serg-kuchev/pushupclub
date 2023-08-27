from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
bot = Bot(token='6664732777:AAFGNe__b2bXVjAClcloauJCt8_Jm7mHGwA')
dp = Dispatcher(bot, storage=MemoryStorage())