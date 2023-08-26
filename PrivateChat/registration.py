from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import connect, cursor
from dispatcher import dp
from PrivateChat.fn import check_timezone
from datetime import datetime, timedelta
import pytz


class Register(StatesGroup):
    password = State()
    name = State()
    nickname = State()
    about = State()
    utc = State()


class EditTimezone(StatesGroup):
    timezone = State()


@dp.callback_query_handler(Text(equals='register'))
async def register(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer('Введи пароль')
    await Register.password.set()


@dp.message_handler(state=Register.password)
async def register_password(message: types.Message, state: FSMContext):
    print(message.text)
    if int(message.text) == 335577:
        await Register.next()
        await message.answer('Введи своё имя')
    else:
        await message.answer('Пароль неверен')
        await state.finish()


@dp.message_handler(state=Register.name)
async def register_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await Register.next()
    await message.answer('Теперь введи свой никнейм')


@dp.message_handler(state=Register.nickname)
async def register_nickname(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await Register.next()
    await message.answer('Напиши о себе')


@dp.message_handler(state=Register.about)
async def register_about(message: types.Message, state: FSMContext):
    await state.update_data(about=message.text)
    await Register.next()
    await message.answer('Введи свой часовой пояс UTC(Если твой пояс часовой пояс UTC +2 введи просто +2\n'
                         'Если твой часовой пояс UTC -3, то введи -3)')


@dp.message_handler(state=Register.utc)
async def register_utc(message: types.Message, state: FSMContext):
    try:
        if check_timezone(message.text):
            await state.update_data(utc=message.text)
            data = await state.get_data()
            try:
                today = datetime.now(pytz.utc) + timedelta(hours=int(data['utc']))
                telegram = f"https://t.me/{message.from_user.username}"
                cursor.execute(f"INSERT INTO users(tg_id, name, nickname, timezone, tg_url, date_start, about) "
                               f"VALUES({message.chat.id},'{data['name']}','{data['nickname']}','{data['utc']}','{telegram}','{today}','{data['about']}')")
                connect.commit()
                await message.answer("Ты успешно зарегистрировался. Для продолжения перейди в основной чат!")
            except Exception as e:
                print(e)
                connect.rollback()
                await message.answer('Что-то пошло не так в процессе регистрации. Обратитесь к администратору')
            await state.finish()
        else:
            raise Exception('ex')
    except:
        await message.answer('Ты ввёл неверный формат UTC, попробуй ещё раз')


@dp.callback_query_handler(Text(equals='change_timezone'))
async def change_timezone(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Введи новый часовой пояс')
    await EditTimezone.timezone.set()


@dp.message_handler(state=EditTimezone.timezone)
async def edit_timezone(message: types.Message, state: FSMContext):
    try:
        if check_timezone(message.text):
            async with state.proxy() as data:
                data['utc'] = message.text
            try:
                cursor.execute(f"UPDATE users SET timezone = '{data['utc']}' WHERE tg_id = {message.chat.id}")
                connect.commit()
                await message.answer("Ты успешно сменил часовой пояс. Для продолжения перейди в основной чат!")
            except:
                connect.rollback()
                await message.answer('Что-то пошло не так в процессе изменения часового пояса. Обратись к администратору')
            await state.finish()
        else:
            raise Exception('ex')
    except:
        await message.answer('Ты ввёл неверный формат UTC, попробуй ещё раз')
