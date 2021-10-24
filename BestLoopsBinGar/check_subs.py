import sqlite3
from datetime import date
from datetime import datetime as dtmp
from datetime import timedelta
sqlite_connection = sqlite3.connect('data.db')
cursor = sqlite_connection.cursor()

today = date.today()
d = today.strftime('%Y-%m-%d')

command = cursor.execute("""SELECT userid, time_subscribe FROM users_data;""") # userid, time_subscribe
data = command.fetchall()

for user in data:
    if user[1] is not None:
        delta = today - dtmp.strptime(user[1], '%Y-%m-%d').date()
        # print(today - datetime.strptime(user[1], '%Y-%m-%d').date())
        if delta > timedelta(days=30, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            # Можно отправлять сообщения если подписка заканчивается))
            print(delta)
            cursor.execute("""UPDATE users_data SET subscriber = ? WHERE userid = ?;""", (0, user[0]))
            sqlite_connection.commit()
cursor.close()

