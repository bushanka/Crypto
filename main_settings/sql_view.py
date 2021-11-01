import sqlite3

sqlite_connection = sqlite3.connect('main_data.db')
cursor = sqlite_connection.cursor()

user_id = 489197056
t = cursor.execute("""SELECT * FROM main_users_data""").fetchall()
print('')
for user in t:
    print(f'ID: {user[0]}')
    print(f'Nick: {user[1]}')
    print(f'Is Subscruber Bin Gar: {user[2]}')
    print(f'Time Subscribed: {user[3]}')
    print()
    print(f'Is Subscruber Bestch Bin: {user[5]}')
    print(f'Time Subscribed: {user[6]}')
    print()
    print('_____________________________________-')
cursor.close()

