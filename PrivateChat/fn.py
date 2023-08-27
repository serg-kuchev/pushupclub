from aiogram import types
from db import cursor, connect


def check_timezone(timezone: str):
    return ((int(timezone) and -12 <= int(timezone) <= 12 and (timezone[0] == '+' or timezone[0] == '-'))
            or timezone == '0')


def get_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    text = ('Ты уже зарегистрирован в проекте!\n'
            'Чтобы изменить настройки выбери:')
    keyboard.inline_keyboard = [
        [types.InlineKeyboardButton('Изменить часовой пояс', callback_data='change_timezone')],
    ]
    if user_id in [503889403, 200570950, 623323275]: #200570950
        cursor.execute("SELECT activity_type FROM activities")
        activities = cursor.fetchone()
        if activities:
            keyboard.inline_keyboard.append([types.InlineKeyboardButton('Редактировать секцию', callback_data='edit_section')])
            keyboard.inline_keyboard.append([types.InlineKeyboardButton('Удалить секцию', callback_data='delete_section')])
    cursor.execute(
        f"SELECT activity_type FROM activities WHERE activity_type NOT IN (SELECT activity FROM user_activities WHERE user_id={user_id})")
    if cursor.fetchone():
        keyboard.inline_keyboard.append([types.InlineKeyboardButton('Записаться на секцию', callback_data='section_register')])
    return text, keyboard