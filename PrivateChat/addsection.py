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
    await callback.message.delete()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cursor.execute(f"SELECT activity_type FROM activities WHERE activity_type NOT IN (SELECT activity FROM user_activities WHERE user_id={callback.message.chat.id})")
    for activity in cursor.fetchall():
        keyboard.inline_keyboard.append([types.InlineKeyboardButton(f"{activity[0]}", callback_data=f"section_register {activity[0]}")])
    keyboard.inline_keyboard.append([types.InlineKeyboardButton('Вернуться в главное меню', callback_data='section_register_back')])
    await callback.message.answer('Выберите секцию, на которую хотите записаться', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "section_register_back")
async def section_register_back(callback: types.CallbackQuery):
    await callback.answer("Вы были возвращены в главное меню")
    await callback.message.delete()
    from PrivateChat.privatemenu import private_start
    await private_start(callback.message)


@dp.callback_query_handler(lambda c: c.data.startswith("section_register "))
async def section_register_concrete(callback: types.CallbackQuery):
    try:
        activity = callback.data.split('section_register ')[1]
        cursor.execute(f"INSERT INTO user_activities(user_id, activity) VALUES({callback.message.chat.id},'{activity}')")
        connect.commit()
        await callback.message.edit_text(f"Вы были успешно зарегистрированы на секцию {activity}")
    except Exception as e:
        print(e)
        connect.rollback()
        await callback.message.edit_text(f'При записи на секцию произошла ошибка\n'
                                         f'Обратитесь с проблемой к администратору!')
