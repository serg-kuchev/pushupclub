import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import connect, cursor
from dispatcher import dp
from PrivateChat.fn import check_timezone
from datetime import date


@dp.callback_query_handler(lambda c: c.data == 'section_register')
async def section_register(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cursor.execute(f"SELECT activity_type FROM activities WHERE activity_type NOT IN (SELECT activity FROM user_activities WHERE user_id={callback.message.chat.id} AND status={True})")
    for activity in cursor.fetchall():
        keyboard.inline_keyboard.append([types.InlineKeyboardButton(f"{activity[0]}", callback_data=f"section_register {activity[0]}")])
    keyboard.inline_keyboard.append([types.InlineKeyboardButton('Вернуться в главное меню', callback_data='section_register_back')])
    user_message = await callback.message.answer('Выберите секцию, на которую хотите записаться', reply_markup=keyboard)
    try:
        cursor.execute(
            f"UPDATE users SET menustatus={True}, menumessage={user_message.message_id} WHERE tg_id={callback.message.chat.id}")
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()


@dp.callback_query_handler(lambda c: c.data == "section_register_back")
async def section_register_back(callback: types.CallbackQuery):
    try:
        cursor.execute(
            f"UPDATE users SET menustatus={False}, menumessage = NULL WHERE tg_id={callback.message.chat.id}")
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()
    await callback.answer("Ты был возвращён в главное меню")
    try:
        await callback.message.delete()
    except:
        pass
    from PrivateChat.privatemenu import private_start
    await private_start(callback.message)


@dp.callback_query_handler(lambda c: c.data.startswith("section_register "))
async def section_register_concrete(callback: types.CallbackQuery):
    try:
        activity = callback.data.split('section_register ')[1]
        cursor.execute(f"SELECT status FROM user_activities WHERE user_id={callback.message.chat.id} AND activity ={activity}")
        if not cursor.fetchone():
            cursor.execute(f"INSERT INTO user_activities(user_id, activity) VALUES({callback.message.chat.id},'{activity}')")
            connect.commit()
        else:
            cursor.execute(f"UPDATE user_activities SET status={True} WHERE user_id={callback.message.chat.id}")
            connect.commit()
        await callback.message.edit_text(f"Ты успешно зарегистрирован в челлендже «{activity}»")
    except Exception as e:
        print(e)
        connect.rollback()
        await callback.message.edit_text(f'При записи на секцию произошла ошибка\n'
                                         f'Обратитесь с проблемой к администратору!')
    try:
        cursor.execute(
            f"UPDATE users SET menustatus={False}, menumessage = NULL WHERE tg_id={callback.message.chat.id}")
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()
