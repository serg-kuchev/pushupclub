from dispatcher import bot
from db import cursor, connect


async def print_wasted():
    from main import service
    cursor.execute("SELECT DISTINCT activity_type, gid, sp_id, thread_id FROM activities")
    activities = cursor.fetchall()
    for activity in activities:
        wasted = []
        cursor.execute(f"SELECT gs_id FROM user_activities WHERE gs_id is not NULL AND activity='{activity[0]}'")
        maximum = cursor.fetchall()
        for i in range(len(maximum)):
            result = service.spreadsheets().values().get(spreadsheetId=activity[2],
                                                         range=f"Календарь!{maximum[i][0]}5").execute()
            w1 = result.get('values')[0]
            cursor.execute(f"SELECT str_id FROM activities WHERE activity_type='{activity[0]}'")
            current_str = cursor.fetchone()[0]
            result = service.spreadsheets().values().get(spreadsheetId=activity[2],
                                                         range=f"Календарь!{maximum[i][0]}{current_str - 1}").execute()
            try:
                w2 = result.get('values')[0]
            except:
                retard = '@' + w1[0].split('https://t.me/')[1]
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