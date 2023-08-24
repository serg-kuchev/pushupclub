from aiogram import types


def check_timezone(timezone: str):
    return ((int(timezone) and -12 <= int(timezone) <= 12 and (timezone[0] == '+' or timezone[0] == '-'))
            or timezone == '0')


def get_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    text = 'Ты уже зарегистрирован в проекте!\n' \
           'Для изменения часового пояса нажми кнопку ниже'
    if user_id == 503889403:
        keyboard.inline_keyboard = [
            [types.InlineKeyboardButton('Добавить новую таблицу', callback_data='add_new_activity')]
        ]
        text = 'Для редактирования таблиц нажмите кнопки ниже'
    else:
        keyboard.inline_keyboard = [
            [types.InlineKeyboardButton('Изменить часовой пояс', callback_data='change_timezone')]
        ]
    return text, keyboard