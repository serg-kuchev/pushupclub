import re
import psycopg2
import pytz
from datetime import datetime, timedelta
connect = psycopg2.connect(dbname='sportbd', user='postgres',
                           password='123321', host='localhost')
cursor = connect.cursor()
def f():
    from main import service
    results = service.spreadsheets().values().batchUpdate(spreadsheetId="1URvbiv6YTMUWTOb5Fb8c5Vl46gtiWe1Zgy4H2TtpTrY", body={
        "valueInputOption": "RAW",
        "data": [
            {"range": f"Календарь!C47", 'values': [[25]]}]}).execute()

f()



# from main import service
# cursor.execute("SELECT DISTINCT activity_type, gid, sp_id, thread_id FROM activities")
# activities = [['PUSH UP CLUB', 1283504748, '1FzzvjBymlduQWL8u-PsKlT5kLpFbf4xOSUq7F0KVJoE', 234, 'AC', 57],['PULL UP CLUB', 2005405281, '196QaUYkTD81PhOgmqxcVXj-ZiTTnEXZQMLKl84zoRfc', 234, 'C', 12],['PLANK CLUB', 1350440039, '1PowSwcQkgVHRnYaQ9N3fUUh7_BWf_GdQ_B3tStgTqeQ', 234, 'C', 12],['PRESS', 1273427716, '1vMXgI67PRx1rCO0N1u_Fcp7RC4JRitbzcxGXEUcSla0', 234, 'H', 12]]
# for activity in activities:
#     wasted = []
#     today = datetime.now(pytz.timezone("Etc/GMT+12")) - timedelta(minutes=22)
#     maximum = activity[4]
#     result = service.spreadsheets().values().get(spreadsheetId=activity[2],
#                                                  range=f"Календарь!B5:{maximum}5", ).execute()
#     w1 = result.get('values')[0]
#     current_str = activity[5]
#     result = service.spreadsheets().values().get(spreadsheetId=activity[2],
#                                                  range=f"Календарь!B{current_str - 1}:{maximum}{current_str - 1}").execute()
#     try:
#         values = result.get('values')[0]
#     except:
#         values = []
#         for i in range(len(w1)):
#             values.append('')
#     result = service.spreadsheets().values().get(spreadsheetId=activity[2],
#                                                  range=f"Календарь!B8:{maximum}8").execute()
#     user = result.get('values')[0]
#     difference = len(user) - len(values)
#     wasted_users_date = []
#     wasted_users = []
#     for i in range(difference):
#         values.append('')
#     for z in range(len(values)):
#         if values[z] == '':
#             wasted_users.append(w1[z])
#             wasted_users_date.append(user[z])
#     for x in range(len(wasted_users_date)):
#         try:
#             user_refactored = datetime.strptime(wasted_users_date[x], "%d.%m.%Y")
#         except:
#             user_refactored = datetime.strptime(wasted_users_date[x], "%d.%m.%y")
#         pytz_refactored = pytz.timezone("Etc/GMT+12").localize(user_refactored)
#         if pytz_refactored < today:
#             print(pytz_refactored, '<>', today)
#             retard = '@' + wasted_users[x].split('https://t.me/')[1]
#             wasted.append(retard)
#     print(wasted,activity[4])


# cursor.execute("SELECT join_date FROM user_activities WHERE user_id=503889403")
# dates = cursor.fetchall()
# maximum = None
# today = datetime.today().date()
# for date in dates:
#     if date[0]:
#         picked_date = datetime.strptime(str(date[0]), "%Y-%m-%d") + timedelta(days=21)
#         if picked_date.date() <= today:
#             maximum = date
#
# if maximum:
#     print("fine")


#cursor.execute(f"SELECT status FROM user_activities WHERE activity='приседания' AND column_id = {0 + 1}")
#if cursor.fetchone()[0]:
    #print("registered")

# cursor.execute(f"SELECT status FROM user_activities WHERE user_id=503889403 AND activity='приседания'")
# status = cursor.fetchone()
# print(status)
# if not status:
#         print('worked')
# else:
#     if not status[0]:
#         print("worked 2")

#cursor.execute(f"INSERT INTO user_activities(user_id, activity, join_date) VALUES(503889403, 'отжимания', '{datetime.now(pytz.timezone('Etc/GMT+3')).date()}')")
#connect.commit()


print(datetime.today().date())