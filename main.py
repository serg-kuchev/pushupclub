import logging
import time
from datetime import datetime
from aiogram.utils import executor
from google.oauth2.service_account import Credentials
from PrivateChat.privatemenu import *
from googleapiclient.discovery import build
from GroupChat.threadobserver import *
from GroupChat.wasted import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
import re
import asyncio


logging.basicConfig(level=logging.INFO)
CREDENTIALS_FILE = 'CredFile'
credentials = Credentials.from_service_account_file('CredFile', scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
service = build('sheets', 'v4', credentials=credentials)


# Handler for messages
@dp.message_handler(content_types=["video", "document", "animation"])
async def set_activity(message: types.Message):
    if not message.is_topic_message:
        return
    if message.caption is not None:
        if not re.match(r'#\d', message.caption):
            return
    else:
        return
    cursor.execute(f"SELECT * FROM users WHERE tg_id={message.from_user.id}")
    if not cursor.fetchone():
        await message.answer("Ты не зарегистрирован в проекте, для участия пройди регистрацию по ссылке ниже\n"
                             "https://t.me/upclubot")
        return
    cursor.execute(f"SELECT activity_type FROM activities WHERE thread_id={message.message_thread_id}")
    activity = cursor.fetchone()[0]
    cursor.execute(f"SELECT status FROM user_activities WHERE user_id={message.from_user.id} AND activity='{activity}'")
    status = cursor.fetchone()
    if not status:
        await message.answer("Ты не зарегистрирован в секции, для участия пройди регистрацию по ссылке ниже\n"
                             "https://t.me/upclubot")
        return
    else:
        if not status[0]:
            await message.answer("Ты не зарегистрирован в секции, для участия пройди регистрацию по ссылке ниже\n"
                                 "https://t.me/upclubot")
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
        cursor.execute(f"SELECT gs_id, join_date FROM user_activities WHERE user_id={message.from_user.id} and activity='{activ[0]}'")
        gs_id = cursor.fetchone()
        match = re.search(r'#(\d+)', message.caption)
        number = int(match.group(1))
        if gs_id[0]:
            if gs_id[1] is None:
                cursor.execute(
                    f"SELECT id,name,nickname,tg_url,timezone,about FROM users WHERE tg_id={message.from_user.id}")
                info = cursor.fetchone()
                current_day = datetime.utcnow().date() + timedelta(hours=int(info[4]))
                current_day_refactored = datetime.strptime(str(current_day), "%Y-%m-%d")
                cursor.execute(f"UPDATE user_activities SET join_date={current_day_refactored.date()} WHERE user_id={message.from_user.id} AND activity='{activ[0]}'")
                connect.commit()
            results = service.spreadsheets().values().batchUpdate(spreadsheetId=activ[3], body={
                "valueInputOption": "RAW",
                "data": [
                    {"range": f"Календарь!{gs_id[0]}{activ[2]+string_index}", 'values': [[number]]}]}).execute()
        else:
            cursor.execute(f"SELECT max(column_id) from user_activities WHERE activity='{activ[0]}'")
            max_column = cursor.fetchone()[0]
            if max_column:
                cursor.execute(f"SELECT gs_id FROM user_activities WHERE column_id = {max_column} and activity='{activ[0]}' ORDER BY column_id DESC")
                maximum = cursor.fetchone()
            else:
                maximum = None
            if maximum:
                temp = maximum[0]
                if temp == "Z" or len(temp) == 2:
                    if temp == "Z":
                        temp = chr(65) + chr(65)
                    elif len(temp) == 2 and temp[1] == 'Z':
                        temp = chr(ord(temp[0]) + 1) + chr(65)
                    elif len(temp) == 2:
                        temp = chr(ord(temp[0])) + chr(ord(temp[1]) + 1)
                else:
                    temp = chr(ord(temp[0]) + 1)
            else:
                temp = chr(66)
            cursor.execute(
                f"SELECT id,name,nickname,tg_url,timezone,about FROM users WHERE tg_id={message.from_user.id}")
            info = cursor.fetchone()
            current_day = datetime.utcnow().date() + timedelta(hours=int(info[4]))
            current_day_refactored = datetime.strptime(str(current_day), "%Y-%m-%d")
            try:
                if temp != chr(66):
                    cursor.execute(
                        f"UPDATE user_activities SET gs_id='{temp}', column_id={max_column + 1}, join_date={current_day_refactored.date()} WHERE user_id={message.from_user.id} AND activity='{activ[0]}'")
                else:
                    cursor.execute(
                        f"UPDATE user_activities SET gs_id='{temp}', column_id={1}, join_date={current_day_refactored.date()} WHERE user_id={message.from_user.id} AND activity='{activ[0]}'")
                connect.commit()
            except Exception as e:
                print(e)
                connect.rollback()
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
            try:
                results = service.spreadsheets().values().batchUpdate(spreadsheetId=activ[3], body={
                    "valueInputOption": "RAW",
                    "data": [
                        {"range": f"Календарь!{temp}3:{temp}7",
                         'values': [[info[1]], [info[2]], [info[3]], ["UTC " + str(info[4])], [info[5]]]},
                        {"range": f"Календарь!{temp}8", 'values': [[f"{current_day_refactored.strftime('%d.%m.%y')}"]]},
                        {"range": f"Календарь!{temp}{activ[2] + string_index}", 'values': [[number]]}]}).execute()
            except Exception as e:
                print("internal server error\nretry in 30 seconds...",e)
                await asyncio.sleep(30)
                results = service.spreadsheets().values().batchUpdate(spreadsheetId=activ[3], body={
                    "valueInputOption": "RAW",
                    "data": [
                        {"range": f"Календарь!{temp}3:{temp}7",
                         'values': [[info[1]], [info[2]], [info[3]], ["UTC " + str(info[4])], [info[5]]]},
                        {"range": f"Календарь!{temp}8", 'values': [[f"{current_day_refactored.strftime('%d.%m.%y')}"]]},
                        {"range": f"Календарь!{temp[0]}{activ[2] + string_index}", 'values': [[number]]}]}).execute()


def main():
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        # Здесь можно добавить логирование ошибки
        print(f"Failed while getting updates: {str(e)}\nBot will restart in 60 seconds")
        time.sleep(60)
        main()


if __name__ == '__main__':
    scheduler = AsyncIOScheduler(timezone=pytz.timezone("Etc/GMT+12"))
    scheduler.add_job(print_wasted, trigger='cron', hour=0, minute=0, second=0,
                      start_date=datetime.now(pytz.timezone("Etc/GMT+12")))
    scheduler.start()
    scheduler2 = AsyncIOScheduler(timezone=pytz.utc)
    scheduler2.add_job(increment_activity_str, trigger='cron', hour=0, minute=0, second=0,
                       start_date=datetime.now(pytz.utc))
    scheduler2.start()
    main()
