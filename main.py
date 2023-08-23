from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import ContentType
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ParseMode
from aiogram.utils import executor
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import psycopg2

#AIzaSyATqFOTz3ToTkDviXZRYu5L58-3mHMoQxI

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token='6200017899:AAFxYqe2-BiBU_k0HsZLnGTWZ-pYBMbGeUQ')
dp = Dispatcher(bot, storage=MemoryStorage())
sp_id = "1KAY73XEKsV4H-TL4jPRqAR6CIm5rIR79ZNkeJEpn0qk"
CREDENTIALS_FILE = 'sportbot-396814-5f4c6812d902.json'
credentials = Credentials.from_service_account_file('sportbot-396814-5f4c6812d902.json', scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
service = build('sheets', 'v4', credentials=credentials)
connect = psycopg2.connect(dbname='sportbd', user='postgres',
                           password='123321', host='localhost')
cursor = connect.cursor()


class Register(StatesGroup):
    name = State()
    UTС = State()


class EditTimezone(StatesGroup):
    timezone = State()


@dp.message_handler(chat_type='private', commands=['start'])
async def private_start(message: types.Message):
    cursor.execute(f"SELECT * FROM users WHERE tg_id={message.from_user.id}")
    users = cursor.fetchone()
    if users:
        keyboard = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [types.InlineKeyboardButton('Изменить часовой пояс', callback_data='change_timezone')]
        ])
        await message.answer('Ты уже зарегистрирован в проекте!\n'
                             'Для изменения часового пояса нажми кнопку ниже', reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [types.InlineKeyboardButton('Да', callback_data='register')]
        ])
        await message.answer('Привет, хочешь ли ты зарегистрироваться в проекте?', reply_markup=keyboard)


@dp.callback_query_handler(Text(equals='register'))
async def register(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer('Введите ваше имя')
    await Register.name.set()


@dp.message_handler(state=Register.name)
async def register_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Register.next()
    await message.answer('Введи ваш часовой пояс UTC(Если твой пояс часовой пояс UTC +2 введи просто +2\n'
                         'Если твой часовой пояс UTC -3, то введи -3)')


@dp.message_handler(state=Register.UTС)
async def register_utc(message: types.Message, state: FSMContext):
    try:
        if (int(message.text) and -12 <= int(message.text) <= 12 and (message.text[0] == '+' or '-')) or message.text == '0':
            async with state.proxy() as data:
                data['utc'] = message.text
            try:
                cursor.execute(f"INSERT INTO users(tg_id, name, timezone) VALUES({message.chat.id},'{data['name']}','{data['utc']}')")
                connect.commit()
                await message.answer("Вы успешно зарегистрировались. Для продолжения перейдите в основной чат!")
            except:
                connect.rollback()
                await message.answer('Что-то пошло не так в процессе регистрации. Обратитесь к администратору')
            await state.finish()
        else:
            raise Exception('ex')
    except:
        await message.answer('Вы ввели неверный формат UTC, попробуйте ещё раз')


@dp.callback_query_handler(Text(equals='change_timezone'))
async def change_timezone(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Введи новый часовой пояс')
    await EditTimezone.timezone.set()


@dp.message_handler(state=EditTimezone.timezone)
async def editTimezone_timezone(message: types.Message, state: FSMContext):
    try:
        if (int(message.text) and -12 <= int(message.text) <= 12 and (message.text[0] == '+' or '-')) or message.text == '0':
            async with state.proxy() as data:
                data['utc'] = message.text
            try:
                cursor.execute(f"UPDATE users SET timezone = '{data['utc']}' WHERE tg_id = {message.chat.id}")
                connect.commit()
                await message.answer("Вы успешно обновили часовой пояс. Для продолжения перейдите в основной чат!")
            except:
                connect.rollback()
                await message.answer('Что-то пошло не так в процессе изменения часового пояса. Обратитесь к администратору')
            await state.finish()
        else:
            raise Exception('ex')
    except:
        await message.answer('Вы ввели неверный формат UTC, попробуйте ещё раз')



# Handler for commands
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне сообщение и я попробую найти автора по ключевым словам в сообщении.")



# Handler for messages
@dp.message_handler(Text(contains="#отжимания"), content_types=["video", "document"])
async def search_author(message: types.Message):
    cursor.execute(f"SELECT timezone FROM users WHERE tg_id={message.from_user.id}")
    timezone = cursor.fetchone()
    if datetime.utcnow().time().hour + int(timezone[0]) <= 12:
        cursor.execute(f"SELECT date FROM tech_info")
        temp = cursor.fetchone()
        if datetime.today().date() != temp[0]:
            a = datetime.today().date() - temp[0]
            cursor.execute(f"UPDATE tech_info SET str_id=str_id+{a.days}, date='{datetime.today().date()}'")
            connect.commit()
        cursor.execute("SELECT str_id FROM tech_info")
        str_id = cursor.fetchone()
        cursor.execute(f"SELECT gs_id FROM users WHERE id={message.from_user.id}")
        gs_id = cursor.fetchone()
        if gs_id[0] is None:
            cursor.execute(f"SELECT gs_id FROM users WHERE gs_id is not NULL ORDER BY id DESC")
            maximum = cursor.fetchone()[0]
            if maximum == "Z" or len(maximum) == 2:
                if maximum[1] == "Z":
                    maximum = chr(ord(maximum[0]) + 1) + chr(65)
                elif len(maximum) == 2:
                    maximum = chr(ord(maximum[0])) + chr(ord(maximum[1]) + 1)
                else:
                    maximum = chr(65) + chr(65)
            else:
                maximum = chr(ord(maximum[0]) + 1)
            cursor.execute(f"UPDATE users SET gs_id={maximum} WHERE tg_id={message.from_user.id}")
            connect.commit()
            request = {
                'requests': [
                    {
                        'appendDimension': {
                            'sheetId': 867585341,
                            'dimension': 'COLUMNS',
                            'length': 1
                        }
                    }
                ]
            }
            rs = service.spreadsheets().batchUpdate(spreadsheetId=sp_id, body=request).execute()
            cursor.execute(f"SELECT name FROM users WHERE tg_id={message.from_user.id}")
            name = cursor.fetchone()[0]
            results = service.spreadsheets().values().batchUpdate(spreadsheetId=sp_id, body={
                "valueInputOption": "RAW",
                "data": [
                    {"range": f"Календарь!{maximum}3", 'values': [[name]]},
                    {"range": f"Календарь!{maximum}{str_id[0]}", 'values': [["да"]]}]}).execute()
        else:
            results = service.spreadsheets().values().batchUpdate(spreadsheetId=sp_id, body={
                "valueInputOption": "RAW",
                "data": [
                    {"range": f"Календарь!{gs_id[0]}{str_id[0]}", 'values': [["да"]]}]}).execute()
    else:
        await bot.send_message(message.chat.id, "Извините, вы опоздали")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)