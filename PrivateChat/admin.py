from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import connect, cursor
from dispatcher import dp



class Activity(StatesGroup):
    gid = State()
    sp_id = State()
    #begin_str = State()


@dp.callback_query_handler(lambda c: c.data.startswith('decline_activity'))
async def decline_activity(callback: types.CallbackQuery):
    activity = callback.data.split(' ')
    try:
        cursor.execute(f"DELETE FROM activities WHERE thread_id = {int(activity[2])}")
        connect.commit()
        await callback.message.edit_text(f"Таблица {activity[1]} была отклонена")
    except Exception as e:
        print(e)
        connect.rollback()
        await callback.message.edit_text(f'При отклонении таблицы произошла ошибка\n{e}\nОбратитесь с проблемой к разработчикам!')
    try:
        cursor.execute(
            f"UPDATE users SET menustatus={False}, menumessage = NULL WHERE tg_id={callback.message.chat.id}")
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()


@dp.callback_query_handler(lambda c: c.data.startswith('accept_activity'))
async def accept_activity(callback: types.CallbackQuery, state: FSMContext):
    activity = callback.data.split('~')
    await state.update_data(activity_type=activity[1], thread_id=int(activity[2]))
    await Activity.gid.set()
    await callback.message.edit_text('Добавьте gid номер листа(располагается в самом конце)')


@dp.message_handler(state=Activity.gid)
async def activity_gid(message: types.Message, state: FSMContext):
    await state.update_data(gid=message.text)
    await Activity.next()
    await message.answer('Укажите sp_id документа, который расположен в ссылке после /d/')


@dp.message_handler(state=Activity.sp_id)
async def activity_type(message: types.Message, state: FSMContext):
    await state.update_data(sp_id=message.text)
    data = await state.get_data()
    await state.finish()
    try:
        cursor.execute(f"UPDATE activities SET gid='{data['gid']}', sp_id='{data['sp_id']}', str_id=9 WHERE thread_id={data['thread_id']}")
        connect.commit()
        await message.answer(f"Таблица {data['activity_type']} успешно создана")
    except Exception as e:
        print(e)
        connect.rollback()
        await message.answer(f'При создании таблицы произошла ошибка\n{e}\nОбратитесь с проблемой к разработчикам!')
    try:
        cursor.execute(
            f"UPDATE users SET menustatus={False}, menumessage = NULL WHERE tg_id={message.chat.id}")
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()


@dp.callback_query_handler(lambda c: c.data == 'delete_section')
async def delete_section(callback: types.CallbackQuery):
    await callback.message.delete()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cursor.execute("SELECT activity_type from activities")
    buttons = []
    at = cursor.fetchall()
    for i in range(len(at)):
        buttons.append(types.InlineKeyboardButton(f"{at[i][0]}", callback_data=f"delete_section~{at[i][0]}"))
    keyboard.add(*buttons)
    user_message = await callback.message.answer("Выберите тип активности для удаления", reply_markup=keyboard)
    try:
        cursor.execute(
            f"UPDATE users SET menustatus={True}, menumessage={user_message.message_id} WHERE tg_id={callback.message.chat.id}")
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()


@dp.callback_query_handler(lambda c: c.data.startswith("delete_section~"))
async def delete_section_concrete(callback: types.CallbackQuery):
    await callback.message.delete()
    cursor.execute(f"DELETE FROM user_activities WHERE activity='{callback.data.split('~')[1]}'")
    connect.commit()
    cursor.execute(f"DELETE FROM activities WHERE activity_type='{callback.data.split('~')[1]}'")
    connect.commit()
    await callback.message.answer('Секция была успешно удалена')
    try:
        cursor.execute(
            f"UPDATE users SET menustatus={False}, menumessage = NULL WHERE tg_id={callback.message.chat.id}")
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()


@dp.callback_query_handler(lambda c: c.data == 'edit_section')
async def edit_section(callback: types.CallbackQuery):
    await callback.message.delete()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cursor.execute("SELECT activity_type, thread_id from activities")
    activities = cursor.fetchall()
    for activity in activities:
        keyboard.inline_keyboard.append([types.InlineKeyboardButton(f"{activity[0]}", callback_data=f"edit_section~{activity[0]}~{activity[1]}")])
    user_message = await callback.message.answer("Выберите секцию для редактирования\nПри нажатии необходимо будет пройти повторную регистрацию таблицы", reply_markup=keyboard)
    try:
        cursor.execute(
            f"UPDATE users SET menustatus={True}, menumessage={user_message.message_id} WHERE tg_id={callback.message.chat.id}")
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()


@dp.callback_query_handler(lambda c: c.data.startswith("edit_section~"))
async def edit_section_concrete(callback: types.CallbackQuery, state: FSMContext):
    activity = callback.data.split('~')
    await state.update_data(activity_type=activity[1], thread_id=int(activity[2]))
    await Activity.gid.set()
    await callback.message.edit_text('Добавьте gid номер листа(располагается в самом конце)')
