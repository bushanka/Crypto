import sqlite3
from datetime import date

sqlite_connection = sqlite3.connect('data.db')
cursor = sqlite_connection.cursor()

user_id = 489197056
today = date.today()
d = today.strftime('%Y-%m-%d')

cursor.execute("""UPDATE users_data SET subscriber = ? WHERE userid = ?;""", (1, user_id))
cursor.execute("""UPDATE users_data SET time_subscribe = ? WHERE userid = ?;""", (d, user_id))
cursor.execute("""UPDATE users_data SET test_access = ? WHERE userid = ?;""",('No', user_id) )
#cursor.execute("""DELETE FROM users_data WHERE userid = 489197056""")
sqlite_connection.commit()
cursor.close()
