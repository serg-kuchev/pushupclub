from dispatcher import bot
from db import cursor, connect
from datetime import datetime, timedelta
import pytz


async def print_wasted():
    from main import service
    cursor.execute("SELECT DISTINCT activity_type, gid, sp_id, thread_id FROM activities")
    activities = cursor.fetchall()
    for activity in activities:
        wasted = []
        today = datetime.now(pytz.timezone("Etc/GMT+12")) - timedelta(minutes=1)
        cursor.execute(f"SELECT max(column_id) from user_activities WHERE activity='{activity[0]}'")
        max_column = cursor.fetchone()[0]
        cursor.execute(
            f"SELECT gs_id FROM user_activities WHERE column_id = {max_column} and activity='{activity[0]}' ORDER BY column_id DESC")
        maximum = cursor.fetchone()[0]
        result = service.spreadsheets().values().get(spreadsheetId=activity[2],
                                                     range=f"Календарь!B5:{maximum}5",).execute()
        w1 = result.get('values')[0]
        cursor.execute(f"SELECT str_id FROM activities WHERE activity_type='{activity[0]}'")
        current_str = cursor.fetchone()[0]
        result = service.spreadsheets().values().get(spreadsheetId=activity[2],
                                                     range=f"Календарь!B{current_str-1}:{maximum}{current_str - 1}").execute()
        try:
            values = result.get('values')[0]
        except:
            values = []
            for i in range(len(w1)):
                values.append('')
        result = service.spreadsheets().values().get(spreadsheetId=activity[2],
                                                     range=f"Календарь!B8:{maximum}8").execute()
        user = result.get('values')[0]
        difference = len(user) - len(values)
        wasted_users_date = []
        wasted_users = []
        for i in range(difference):
            values.append('')
        for z in range(len(values)):
            if values[z] == '':
                cursor.execute(f"SELECT status FROM user_activities WHERE activity='{activity[0]}' AND column_id = {z + 1}")
                if cursor.fetchone()[0]:
                    wasted_users.append(w1[z])
                    wasted_users_date.append(user[z])
        for x in range(len(wasted_users_date)):
            try:
                user_refactored = datetime.strptime(wasted_users_date[x], "%d.%m.%Y")
            except:
                user_refactored = datetime.strptime(wasted_users_date[x], "%d.%m.%y")
            pytz_refactored = pytz.timezone("Etc/GMT+12").localize(user_refactored)
            if pytz_refactored < today:
                retard = '@' + wasted_users[x].split('https://t.me/')[1]
                wasted.append(retard)
        if wasted:
            wasted_joined = '\n'.join(wasted)
            await bot.send_message(-1001665866587, f"Список Опоздавших в {activity[0]}\n{wasted_joined}", reply_to_message_id=activities[3])


async def increment_activity_str():
    cursor.execute("SELECT activity_type,str_id FROM activities")
    activities = cursor.fetchall()
    for activity in activities:
        cursor.execute(f"UPDATE activities SET str_id = {activity[1] + 1} WHERE activity_type='{activity[0]}'")
        connect.commit()