import psycopg2
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
connect = psycopg2.connect(dbname='sportbd', user='postgres',
                           password='123321', host='localhost')
cursor = connect.cursor()
CREDENTIALS_FILE = 'sportbot-396814-5f4c6812d902.json'
credentials = Credentials.from_service_account_file('sportbot-396814-5f4c6812d902.json', scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
service = build('sheets', 'v4', credentials=credentials)
# result = service.spreadsheets().values().get(spreadsheetId='1FzzvjBymlduQWL8u-PsKlT5kLpFbf4xOSUq7F0KVJoE',
#                                              range=f"Календарь!B27:K27", valueRenderOption="UNFORMATTED_VALUE").execute()
# values = result.get('values', [])
# data_array = []
# for row in values:
#     for cell in row:
#         data_array.append(cell)

# выводим массив с данными
# print(data_array)
# print(values)
wasted = []
today = datetime.now(pytz.timezone("Etc/GMT+12")) - timedelta(minutes=1)
cursor.execute(f"SELECT max(column_id) from user_activities WHERE activity='{activity[0]}'")
max_column = cursor.fetchone()[0]
cursor.execute(
    f"SELECT gs_id FROM user_activities WHERE column_id = {max_column} and activity='{activity[0]}' ORDER BY column_id DESC")
maximum = cursor.fetchone()[0]
result = service.spreadsheets().values().get(spreadsheetId=activity[2],
                                             range=f"Календарь!B5:{maximum}5", ).execute()
w1 = result.get('values')[0]
cursor.execute(f"SELECT str_id FROM activities WHERE activity_type='{activity[0]}'")
current_str = cursor.fetchone()[0]
result = service.spreadsheets().values().get(spreadsheetId=activity[2],
                                             range=f"Календарь!B{current_str - 1}:{maximum}{current_str - 1}").execute()
values = result.get('values')[0]
result = service.spreadsheets().values().get(spreadsheetId=activity[2],
                                             range=f"Календарь!B8:{maximum}8").execute()
user = result.get('values')[0]
difference = len(user) - len(values)
wasted_users = []
for i in range(difference):
    values.append('')
for z in range(len(values)):
    if values[z] == '':
        wasted_users.append(user[z])
for x in range(len(user)):
    try:
        user_refactored = datetime.strptime(wasted_users[x], "%d.%m.%Y")
    except:
        user_refactored = datetime.strptime(wasted_users[x], "%d.%m.%y")
    pytz_refactored = pytz.timezone("Etc/GMT+12").localize(user_refactored)
    if pytz_refactored < today:
        retard = '@' + w1[0].split('https://t.me/')[1]
        wasted.append(retard)
