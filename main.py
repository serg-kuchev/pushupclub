import logging
from datetime import datetime
from dispatcher import bot
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from google.oauth2.service_account import Credentials
from aiogram.types import ForumTopicCreated, ContentType
from googleapiclient.discovery import build
from PrivateChat.privatemenu import *

# AIzaSyATqFOTz3ToTkDviXZRYu5L58-3mHMoQxI

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
sp_id = "1KAY73XEKsV4H-TL4jPRqAR6CIm5rIR79ZNkeJEpn0qk"
CREDENTIALS_FILE = 'sportbot-396814-5f4c6812d902.json'
credentials = Credentials.from_service_account_file('sportbot-396814-5f4c6812d902.json', scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
service = build('sheets', 'v4', credentials=credentials)


# Handler for commands
@dp.message_handler(chat_type='supergroup', commands=['start'])
async def send_welcome(message: types.Message):
    print(message.forum_topic_created, message.message_thread_id)
    await message.reply("Привет! Отправь мне сообщение и я попробую найти автора по ключевым словам в сообщении.")


# Handler for messages
@dp.message_handler(Text(contains="#отжимания"), content_types=["video", "document"])
async def search_author(message: types.Message):
    cursor.execute(f"SELECT timezone FROM users WHERE tg_id={message.from_user.id}")
    timezone = cursor.fetchone()
    if datetime.utcnow().time().hour + int(timezone[0]) <= 12:
        cursor.execute(f"SELECT date FROM tech_info")
        temp = cursor.fetchone()
        if datetime.today().date() != temp[0]:
            a = datetime.today().date() - temp[0]
            cursor.execute(f"UPDATE tech_info SET str_id=str_id+{a.days}, date='{datetime.today().date()}'")
            connect.commit()
        cursor.execute("SELECT str_id FROM tech_info")
        str_id = cursor.fetchone()
        cursor.execute(f"SELECT gs_id FROM users WHERE id={message.from_user.id}")
        gs_id = cursor.fetchone()
        if gs_id[0] is None:
            cursor.execute(f"SELECT gs_id FROM users WHERE gs_id is not NULL ORDER BY id DESC")
            maximum = cursor.fetchone()[0]
            if maximum == "Z" or len(maximum) == 2:
                if maximum[1] == "Z":
                    maximum = chr(ord(maximum[0]) + 1) + chr(65)
                elif len(maximum) == 2:
                    maximum = chr(ord(maximum[0])) + chr(ord(maximum[1]) + 1)
                else:
                    maximum = chr(65) + chr(65)
            else:
                maximum = chr(ord(maximum[0]) + 1)
            cursor.execute(f"UPDATE users SET gs_id={maximum} WHERE tg_id={message.from_user.id}")
            connect.commit()
            request = {
                'requests': [
                    {
                        'appendDimension': {
                            'sheetId': 867585341,
                            'dimension': 'COLUMNS',
                            'length': 1
                        }
                    }
                ]
            }
            rs = service.spreadsheets().batchUpdate(spreadsheetId=sp_id, body=request).execute()
            cursor.execute(f"SELECT name FROM users WHERE tg_id={message.from_user.id}")
            name = cursor.fetchone()[0]
            results = service.spreadsheets().values().batchUpdate(spreadsheetId=sp_id, body={
                "valueInputOption": "RAW",
                "data": [
                    {"range": f"Календарь!{maximum}3", 'values': [[name]]},
                    {"range": f"Календарь!{maximum}{str_id[0]}", 'values': [["да"]]}]}).execute()
        else:
            results = service.spreadsheets().values().batchUpdate(spreadsheetId=sp_id, body={
                "valueInputOption": "RAW",
                "data": [
                    {"range": f"Календарь!{gs_id[0]}{str_id[0]}", 'values': [["да"]]}]}).execute()
    else:
        await bot.send_message(message.chat.id, "Извините, вы опоздали")


@dp.message_handler(content_types=[ContentType.FORUM_TOPIC_CREATED])
async def topic_created(message: types.Message):
    try:
        cursor.execute(f"INSERT INTO activities(activity_type, thread_id) VALUES('{message.forum_topic_created.name}',{message.message_thread_id})")
        connect.commit()
    except Exception as e:
        connect.rollback()
        await message.answer(f'При регистрации топика произошла ошибка\n{e}\nОбратитесь с проблемой к разработчикам!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)