from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import connect, cursor
from dispatcher import dp


class Activity(StatesGroup):
    spreadsheet = State()
    sp_id = State()


@dp.callback_query_handler(lambda c: c.data == 'add_new_activity')
async def add_new_activity(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Предоставьте ссылку на таблицу')
    await Activity.spreadsheet.set()


@dp.callback_query_handler(lambda c: c.data.startswith('decline_activity'))
async def decline_activity(callback: types.CallbackQuery):
    activity = callback.data.split(' ')
    try:
        cursor.execute(f"DELETE FROM activities WHERE thread_id = {int(activity[2])}")
        connect.commit()
        await callback.message.edit_text(f"Таблица {activity[1]} была отклонена")
    except Exception as e:
        connect.rollback()
        await callback.message.edit_text(f'При отклонении таблицы произошла ошибка\n{e}\nОбратитесь с проблемой к разработчикам!')


@dp.callback_query_handler(lambda c: c.data.startswith('accept_activity'))
async def accept_activity(callback: types.CallbackQuery, state: FSMContext):
    activity = callback.data.split(' ')
    await state.update_data(activity_type=activity[1], thread_id=int(activity[2]))
    await Activity.spreadsheet.set()
    await callback.message.edit_text('Добавьте ссылку на таблицу для её регистрации')


@dp.message_handler(state=Activity.spreadsheet)
async def activity_spreadsheet(message: types.Message, state: FSMContext):
    await state.update_data(spreadsheet=message.text)
    await Activity.next()
    await message.answer('Укажите номер столбца таблицы')


@dp.message_handler(state=Activity.sp_id)
async def activity_type(message: types.Message, state: FSMContext):
    await state.update_data(sp_id=message.text)
    data = await state.get_data()
    await state.finish()
    try:
        cursor.execute(f"UPDATE activities SET spreadsheet='{data['spreadsheet']}', sp_id='{data['sp_id']}' WHERE thread_id={data['thread_id']}")
        connect.commit()
        await message.answer(f"Таблица {data['activity_type']} успешно создана")
    except Exception as e:
        print(e)
        connect.rollback()
        await message.answer(f'При создании таблицы произошла ошибка\n{e}\nОбратитесь с проблемой к разработчикам!')