import psycopg2
import pytz
from datetime import datetime, timedelta
connect = psycopg2.connect(dbname='sportbd', user='postgres',
                           password='123321', host='localhost')
cursor = connect.cursor()


maximum = ''
if maximum:
    temp = maximum
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


print(temp)