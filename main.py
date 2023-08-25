import logging
from datetime import datetime
from aiogram.utils import executor
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from PrivateChat.privatemenu import *
from GroupChat.threadobserver import *
from GroupChat.wasted import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
import re

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
    await message.reply("Привет! Отправь мне сообщение и я попробую найти автора по ключевым словам в сообщении.")


# Handler for messages
@dp.message_handler(Text(startswith="#"), content_types=["video", "document"])
async def set_activity(message: types.Message):
    if not message.is_topic_message:
        return
    cursor.execute(f"SELECT * FROM users WHERE tg_id={message.from_user.id}")
    if not cursor.fetchone:
        await message.answer("Вы не зарегистрированы в проекте, для участия пройдите регистрацию по ссылке ниже\n"
                             "https://t.me/Testing_Enot_bot")
        return
    cursor.execute(f"SELECT timezone FROM users WHERE tg_id={message.from_user.id}")
    timezone = cursor.fetchone()
    #if datetime.utcnow().time().hour + int(timezone[0]) <= 12:
    cursor.execute(f"SELECT date FROM tech_info")
    temp = cursor.fetchone()
    if datetime.today().date() != temp[0]:
        a = datetime.today().date() - temp[0]
        cursor.execute(f"UPDATE tech_info SET str_id=str_id+{a.days}, date='{datetime.today().date()}'")
        connect.commit()
    cursor.execute("SELECT str_id FROM tech_info")
    str_id = cursor.fetchone()
    cursor.execute(f"SELECT gs_id FROM users WHERE tg_id={message.from_user.id}")
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
        cursor.execute(f"UPDATE users SET gs_id='{maximum}' WHERE tg_id={message.from_user.id}")
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
        cursor.execute(f"SELECT id,name,nickname,tg_url,timezone,date_start FROM users WHERE tg_id={message.from_user.id}")
        info = cursor.fetchone()
        results = service.spreadsheets().values().batchUpdate(spreadsheetId=sp_id, body={
            "valueInputOption": "RAW",
            "data": [
                {"range": f"Календарь!{maximum}2:{maximum}6", 'values': [[info[0]], [info[1]], [info[2]], [info[3]], ["UTC " + str(info[4])]]},
                {"range": f"Календарь!{maximum}7", 'values': [[f"{info[5]}"]]},
                {"range": f"Календарь!{maximum}{str_id[0]}", 'values': [["да"]]}]}).execute()
    else:
        results = service.spreadsheets().values().batchUpdate(spreadsheetId=sp_id, body={
            "valueInputOption": "RAW",
            "data": [
                {"range": f"Календарь!{gs_id[0]}{str_id[0]}", 'values': [["да"]]}]}).execute()
    #else:
        #await bot.send_message(message.chat.id, "Извините, вы опоздали", reply_to_message_id=message.message_thread_id)


@dp.message_handler(lambda c: re.match(r'#\d+$', c.text))
async def test(message: types.Message):
    if not message.is_topic_message:
        return
    cursor.execute(f"SELECT * FROM users WHERE tg_id={message.from_user.id}")
    if not cursor.fetchone():
        await message.answer("Вы не зарегистрированы в проекте, для участия пройдите регистрацию по ссылке ниже\n"
                             "https://t.me/Testing_Enot_bot")
        return
    cursor.execute(f"SELECT spreadsheet, sp_id FROM activities WHERE thread_id={message.message_thread_id}")
    count = message.text.split('#')[1]
    print(count)
    gid, sp = cursor.fetchone()
    print(gid, sp)
    await message.answer("Ваш результат был учтён")


if __name__ == '__main__':
    scheduler = AsyncIOScheduler(timezone=pytz.utc)
    scheduler.add_job(print_wasted, trigger='cron', hour=0, minute=0, start_date=datetime.now(pytz.utc))
    scheduler.start()
    executor.start_polling(dp, skip_updates=True)
