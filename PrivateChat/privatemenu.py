from PrivateChat.fn import get_keyboard
from PrivateChat.admin import *
from PrivateChat.registration import *
from PrivateChat.addsection import *
from dispatcher import bot
import gc


@dp.message_handler(lambda c: c.text == "Начать" or c.text == "/start", chat_type='private')
async def private_start(message: types.Message):
    cursor.execute(f"SELECT * FROM users WHERE tg_id={message.chat.id}")
    users = cursor.fetchone()
    if users:
        cursor.execute(f"SELECT menumessage FROM users WHERE tg_id = {message.chat.id}")
        menu_message = cursor.fetchone()[0]
        if menu_message:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=menu_message, text='удалено')
        text, keyboard = get_keyboard(message.chat.id)
        user_message = await message.answer(text, reply_markup=keyboard)
        try:
            cursor.execute(f"UPDATE users SET menustatus={True}, menumessage={user_message.message_id} WHERE tg_id={message.chat.id}")
            connect.commit()
        except Exception as e:
            print(e)
            connect.rollback()
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [types.InlineKeyboardButton('Да', callback_data='register')]
        ])
        await message.answer('Привет !\nХочешь зарегистрироваться в проекте UP CLUB ?', reply_markup=keyboard)
    gc.collect()
