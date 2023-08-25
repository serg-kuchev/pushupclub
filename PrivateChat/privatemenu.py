from PrivateChat.fn import get_keyboard
from PrivateChat.admin import *
from PrivateChat.registration import *


@dp.message_handler(chat_type='private', commands=['start'])
async def private_start(message: types.Message):
    cursor.execute(f"SELECT * FROM users WHERE tg_id={message.from_user.id}")
    users = cursor.fetchone()
    if users:
        text, keyboard = get_keyboard(message.chat.id)
        await message.answer(text, reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [types.InlineKeyboardButton('Да', callback_data='register')]
        ])
        await message.answer('Привет, хочешь ли ты зарегистрироваться в проекте?', reply_markup=keyboard)