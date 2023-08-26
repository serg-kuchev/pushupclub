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
        connect.rollback()
        await callback.message.edit_text(f'При отклонении таблицы произошла ошибка\n{e}\nОбратитесь с проблемой к разработчикам!')


@dp.callback_query_handler(lambda c: c.data.startswith('accept_activity'))
async def accept_activity(callback: types.CallbackQuery, state: FSMContext):
    activity = callback.data.split(' ')
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



# mb future update
# @dp.message_handler(state=Activity.begin_str)
# async def activity_begin_str(message: types.Message, state: FSMContext):
#     await state.update_data(begin_str=message.text)
#     data = await state.get_data()
#     await state.finish()
#     try:
#         cursor.execute(f"UPDATE activities SET gid='{data['gid']}', sp_id='{data['sp_id']}', str_id='{data['begin_str']}' WHERE thread_id={data['thread_id']}")
#         connect.commit()
#         await message.answer(f"Таблица {data['activity_type']} успешно создана")
#     except Exception as e:
#         print(e)
#         connect.rollback()
#         await message.answer(f'При создании таблицы произошла ошибка\n{e}\nОбратитесь с проблемой к разработчикам!')