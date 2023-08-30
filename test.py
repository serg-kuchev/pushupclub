import psycopg2
import pytz
from datetime import datetime, timedelta
connect = psycopg2.connect(dbname='sportbd', user='postgres',
                           password='123321', host='localhost')
cursor = connect.cursor()

from main import service
cursor.execute("SELECT DISTINCT activity_type, gid, sp_id, thread_id FROM activities")
activities = [['PUSH UP CLUB', 1283504748, '1FzzvjBymlduQWL8u-PsKlT5kLpFbf4xOSUq7F0KVJoE', 234]]
for activity in activities:
    print(activity)
    wasted = []
    today = datetime.now(pytz.timezone("Etc/GMT+12")) - timedelta(minutes=1)
    maximum = 'AC'
    result = service.spreadsheets().values().get(spreadsheetId=activity[2],
                                                 range=f"Календарь!B5:{maximum}5", ).execute()
    w1 = result.get('values')[0]
    cursor.execute(f"SELECT str_id FROM activities WHERE activity_type='{activity[0]}'")
    current_str = 57
    result = service.spreadsheets().values().get(spreadsheetId=activity[2],
                                                 range=f"Календарь!B{current_str - 1}:{maximum}{current_str - 1}").execute()
    values = result.get('values')[0]
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
    print(wasted)
    print(w1)
    print(values)
    print(user)