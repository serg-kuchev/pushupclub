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


class EditAbout(StatesGroup):
    about = State()


@dp.callback_query_handler(Text(equals='register'))
async def register(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer('Введи пароль')
    await Register.password.set()


@dp.message_handler(state=Register.password)
async def register_password(message: types.Message, state: FSMContext):
    if message.text == "1111":
        await Register.next()
        await message.answer('Введи своё имя\n(например: Александр)')
    else:
        await message.answer('Пароль неверен\nВведи /start, чтобы снова попробовать')
        await state.finish()


@dp.message_handler(state=Register.name)
async def register_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await Register.next()
    await message.answer('Теперь введи свой никнейм\n(например: Гигачадский)')


@dp.message_handler(state=Register.nickname)
async def register_nickname(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await Register.next()
    await message.answer('Напиши о себе\n(кто ты, чем занимаешься, что нравится: чем подробнее, тем может быть лучше)')


@dp.message_handler(state=Register.about)
async def register_about(message: types.Message, state: FSMContext):
    await state.update_data(about=message.text)
    await Register.next()
    await message.answer('Введи свой часовой пояс UTC\n'
                         '(Если твой пояс часовой пояс UTC+5 введи просто +5, а если UTC-3, то введи -3\n'
                         'Московское время: UTC+3)')


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
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                buttons = ['Начать']
                keyboard.add(*buttons)
                await message.answer("Ты успешно зарегистрировался. Для продолжения перейди в основной чат!", reply_markup=keyboard)
                from PrivateChat.privatemenu import private_start
                await private_start(message)
            except Exception as e:
                print(e)
                connect.rollback()
                await message.answer('Что-то пошло не так в процессе регистрации. Обратись к администратору')
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
                from main import service
                for i in info:
                    rs = service.spreadsheets().values().batchUpdate(spreadsheetId=i[1], body={
                        "valueInputOption": "RAW",
                        "data": [{"range": f"Календарь!{i[0]}6", "values": [['UTC ' + data['utc']]]}]
                    }).execute()
                await message.answer("Ты успешно сменил часовой пояс. Для продолжения перейди в основной чат!")
                try:
                    cursor.execute(
                        f"UPDATE users SET menustatus={False}, menumessage = NULL WHERE tg_id={message.chat.id}")
                    connect.commit()
                except Exception as e:
                    print(e)
                    connect.rollback()
            except Exception as e:
                print(e)
                connect.rollback()
                await message.answer('Что-то пошло не так в процессе изменения часового пояса. Обратись к администратору')
            await state.finish()

        else:
            raise Exception('ex')
    except:
        await message.answer('Ты ввёл неверный формат UTC, попробуй ещё раз')


@dp.callback_query_handler(lambda c: c.data == "edit_about")
async def edit_about_menu(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Введи новую информацию о себе")
    await EditAbout.about.set()


@dp.message_handler(state=EditAbout.about)
async def edit_about(message: types.Message, state: FSMContext):
    try:
        cursor.execute(f"UPDATE users SET about='{message.text}' WHERE tg_id={message.chat.id}")
        connect.commit()
        cursor.execute(
            f"SELECT gs_id, sp_id FROM user_activities JOIN activities ON activity=activity_type WHERE user_id={message.chat.id}")
        info = cursor.fetchall()
        from main import service
        for i in info:
            rs = service.spreadsheets().values().batchUpdate(spreadsheetId=i[1], body={
                "valueInputOption": "RAW",
                "data": [{"range": f"Календарь!{i[0]}7", "values": [[message.text]]}]
            }).execute()
        await message.answer('Ты успешно сменил информацию о себе')
    except Exception as e:
        print(e)
        connect.rollback()
        await message.answer('Что-то пошло не так в процессе изменения информации о себе. Обратись к администратору')
    try:
        cursor.execute(
            f"UPDATE users SET menustatus={False}, menumessage = NULL WHERE tg_id={message.chat.id}")
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()
    await state.finish()
