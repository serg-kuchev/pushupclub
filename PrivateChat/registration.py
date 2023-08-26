from aiogram.dispatcher.filters import Text
from PrivateChat.fn import check_timezone
from datetime import date
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import connect, cursor
from dispatcher import dp


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
                today = date.today()
                telegram = f"https://t.me/{message.from_user.username}"
                cursor.execute(f"INSERT INTO users(tg_id, name, nickname, timezone, tg_url, date_start, about) "
                               f"VALUES({message.chat.id},'{data['name']}','{data['nickname']}','{data['utc']}','{telegram}','{today}','{data['about']}')")
                connect.commit()
                await message.answer("Ты успешно зарегистрировался. Для продолжения перейди в основной чат!")
            except Exception as e:
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
                cursor.execute(f"SELECT gs_id, sp_id FROM user_activities JOIN activities ON activity=activity_type WHERE user_id={message.chat.id}")
                info = cursor.fetchall()
                print(info)
                from main import service
                for i in info:
                    rs = service.spreadsheets().values().batchUpdate(spreadsheetId=i[1], body={
                        "valueInputOption": "RAW",
                        "data": [{"range": f"Календарь!{i[0]}6", "values": [['UTC ' + data['utc']]]}]
                    }).execute()
                await message.answer("Ты успешно сменил часовой пояс. Для продолжения перейди в основной чат!")
            except Exception as e:
                print(e)
                connect.rollback()
                await message.answer('Что-то пошло не так в процессе изменения часового пояса. Обратись к администратору')
            await state.finish()
        else:
            raise Exception('ex')
    except:
        await message.answer('Ты ввёл неверный формат UTC, попробуй ещё раз')


@dp.callback_query_handler(Text(equals='delete_section'))
async def delete_section(callback: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cursor.execute("SELECT activity_type from activities")
    buttons = []
    at = cursor.fetchall()[0]
    for i in range (len(at)):
        buttons.append(types.InlineKeyboardButton(f"{at[i]}", callback_data=f"delete_activity {at[i]}"))
    keyboard.add(*buttons)
    await callback.message.answer("Выберите тип активности для удаления", reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith="delete_activity"))
async def delete_activity(callback: types.CallbackQuery):
    cursor.execute(f"DELETE FROM activities WHERE activity_type={callback.data.split(' ')[1]}")
    connect.commit()
    cursor.execute(f"DELETE FROM user_activities WHERE activity={callback.data.split(' ')[1]}")
    connect.commit()