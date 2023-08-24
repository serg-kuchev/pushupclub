from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import connect, cursor
from dispatcher import dp
from PrivateChat.fn import check_timezone


class Register(StatesGroup):
    name = State()
    utc = State()


class EditTimezone(StatesGroup):
    timezone = State()


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


@dp.message_handler(state=Register.utc)
async def register_utc(message: types.Message, state: FSMContext):
    try:
        if check_timezone(message.text):
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
