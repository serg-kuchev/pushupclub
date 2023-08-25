from aiogram import types
from aiogram.types import ContentType
from db import cursor, connect
from dispatcher import dp, bot


@dp.message_handler(content_types=[ContentType.FORUM_TOPIC_CREATED])
async def topic_created(message: types.Message):
    try:
        topic_name = message.forum_topic_created.name
        thread_id = message.message_thread_id
        cursor.execute(f"INSERT INTO activities(activity_type, thread_id) VALUES('{topic_name}',{thread_id})")
        connect.commit()
        keyboard = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [types.InlineKeyboardButton(f"Добавить таблицу {topic_name}", callback_data=f"accept_activity {topic_name} {thread_id}")],
            [types.InlineKeyboardButton(f"Отменить создание таблицы", callback_data=f"decline_activity {topic_name} {thread_id}")]
        ])
        await bot.send_message(623323275, f"В беседе был создан новый топик с названием {topic_name}\n", reply_markup=keyboard)
    except Exception as e:
        connect.rollback()
        await message.answer(f'При регистрации топика произошла ошибка\n{e}\nОбратитесь с проблемой к разработчикам!')