import re
# import psycopg2
# import pytz
# from datetime import datetime, timedelta
# connect = psycopg2.connect(dbname='sportbd', user='postgres',
#                            password='123321', host='localhost')
# cursor = connect.cursor()
#
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

def trigger(message):
    if message is not None:
        print(f"caption message: {message}")
        if not re.match(r'#\d', message):
            return
    else:
        return
    print("fine")


trigger(None)