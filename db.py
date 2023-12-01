import psycopg2
connect = psycopg2.connect(dbname='dev', user='local',
                           password='local', host='pushup.dev_db')
cursor = connect.cursor()