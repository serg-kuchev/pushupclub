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
logging.basicConfig(level=logging.INFO)
CREDENTIALS_FILE = 'sportbot-396814-5f4c6812d902.json'
credentials = Credentials.from_service_account_file('sportbot-396814-5f4c6812d902.json', scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
service = build('sheets', 'v4', credentials=credentials)


# Handler for commands
@dp.message_handler(content_types=["video", "document"])
async def send_welcome(message: types.Message):
    print("timed")


# Handler for messages
@dp.message_handler(lambda c: re.match(r'#\d', c.caption), content_types=["video", "document"])
async def set_activity(message: types.Message):
    if not message.is_topic_message:
        return
    cursor.execute(f"SELECT * FROM users WHERE tg_id={message.from_user.id}")
    if not cursor.fetchone():
        await message.answer("Вы не зарегистрированы в проекте, для участия пройдите регистрацию по ссылке ниже\n"
                             "https://t.me/Testing_Enot_bot")
        return
    cursor.execute(f"SELECT activity_type FROM activities WHERE thread_id={message.message_thread_id}")
    activity = cursor.fetchone()[0]
    cursor.execute(f"SELECT * FROM user_activities WHERE user_id={message.from_user.id} AND activity='{activity}'")
    if not cursor.fetchone():
        await message.answer("Вы не зарегистрированы в секции, для регистрации пройдите регистрацию по ссылке ниже\n"
                             "https://t.me/Testing_Enot_bot")
        return
    cursor.execute(f"SELECT timezone FROM users WHERE tg_id={message.from_user.id}")
    timezone = cursor.fetchone()
    string_index = 0
    if datetime.utcnow().time().hour + int(timezone[0]) >= 24:
        string_index += 1
    elif datetime.utcnow().time().hour + int(timezone[0]) < 0:
        string_index -= 1
    cursor.execute(f"SELECT activity_type, gid, str_id, sp_id FROM activities WHERE thread_id={message.message_thread_id}")
    activ = cursor.fetchone()
    if activ:
        cursor.execute(f"SELECT gs_id FROM user_activities WHERE user_id={message.from_user.id} and activity='{activ[0]}'")
        gs_id = cursor.fetchone()
        match = re.search(r'#(\d+)', message.caption)
        number = int(match.group(1))
        if gs_id[0]:
            results = service.spreadsheets().values().batchUpdate(spreadsheetId=activ[3], body={
                "valueInputOption": "RAW",
                "data": [
                    {"range": f"Календарь!{gs_id[0]}{activ[2]+string_index}", 'values': [[number]]}]}).execute()
        else:
            cursor.execute(
                f"SELECT gs_id FROM user_activities WHERE gs_id is not NULL and activity='{activ[0]}' ORDER BY id DESC")
            maximum = cursor.fetchone()
            if maximum:
                temp = maximum[0]
                if temp == "Z" or len(temp) == 2:
                    if temp == "Z":
                        temp = chr(ord(temp[0]) + 1) + chr(65)
                    elif len(temp) == 2:
                        temp = chr(ord(temp[0])) + chr(ord(temp[1]) + 1)
                    else:
                        temp = chr(65) + chr(65)
                else:
                    temp = chr(ord(temp[0]) + 1)
            else:
                temp = chr(66)
            cursor.execute(
                f"UPDATE user_activities SET gs_id='{temp}' WHERE user_id={message.from_user.id} AND activity='{activ[0]}'")
            connect.commit()
            request = {
                'requests': [
                    {
                        'appendDimension': {
                            'sheetId': activ[1],
                            'dimension': 'COLUMNS',
                            'length': 1
                        }
                    }
                ]
            }
            rs = service.spreadsheets().batchUpdate(spreadsheetId=activ[3], body=request).execute()
            cursor.execute(
                f"SELECT id,name,nickname,tg_url,timezone,date_start,about FROM users WHERE tg_id={message.from_user.id}")
            info = cursor.fetchone()
            results = service.spreadsheets().values().batchUpdate(spreadsheetId=activ[3], body={
                "valueInputOption": "RAW",
                "data": [
                    {"range": f"Календарь!{temp}3:{temp}7",
                     'values': [[info[1]], [info[2]], [info[3]], ["UTC " + str(info[4])], [info[6]]]},
                    {"range": f"Календарь!{temp}8", 'values': [[f"{info[5]}"]]},
                    {"range": f"Календарь!{temp[0]}{activ[2] + string_index}", 'values': [[number]]}]}).execute()


if __name__ == '__main__':
    scheduler = AsyncIOScheduler(timezone=pytz.timezone("Etc/GMT+12"))
    scheduler.add_job(print_wasted, trigger='cron', hour=0, minute=0, second=0, start_date=datetime.now(pytz.timezone("Etc/GMT+12")))
    scheduler.start()
    scheduler2 = AsyncIOScheduler(timezone=pytz.utc)
    scheduler2.add_job(increment_activity_str, trigger='cron', hour=0, minute=0, second=0, start_date=datetime.now(pytz.utc))
    scheduler2.start()
    executor.start_polling(dp, skip_updates=True)
