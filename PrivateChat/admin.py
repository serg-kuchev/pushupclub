from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import connect, cursor
from dispatcher import dp


class Activity(StatesGroup):
    spreadsheet = State()
    activity_type = State()


@dp.callback_query_handler(lambda c: c.data == 'add_new_activity')
async def add_new_activity(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Предоставьте ссылку на таблицу')
    await Activity.spreadsheet.set()


@dp.message_handler(state=Activity.spreadsheet)
async def activity_spreadsheet(message: types.Message, state: FSMContext):
    await state.update_data(spreadsheet=message.text)
    await Activity.next()
    await message.answer('Введите название таблицы')


@dp.message_handler(state=Activity.activity_type)
async def activity_type(message: types.Message, state: FSMContext):
    await state.update_data(activity_type=message.text)
    data = await state.get_data()
    await state.finish()
    try:
        cursor.execute(f"INSERT INTO activities(spreadsheet, activity_type) VALUES('{data['spreadsheet']}','{data['activity_type']}')")
        connect.commit()
        await message.answer(f"Таблица {data['activity_type']} успешно создана")
    except Exception as e:
        connect.rollback()
        await message.answer(f'При создании таблицы произошла ошибка\n{e}\nОбратитесь с проблемой к разработчикам!')