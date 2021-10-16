import sqlite3

sqlite_connection = sqlite3.connect('data.db')
cursor = sqlite_connection.cursor()

user_id = 489197056
t = cursor.execute("""SELECT * FROM users_data""").fetchall()
print('')
for user in t:
    print(f'ID: {user[0]}')
    print(f'Nick: {user[1]}')
    print(f'Is Subscruber: {user[2]}')
    print(f'Time Subscribed: {user[7]}')
    print(f'Test Access : {user[6]}')
    print(f'Volume : {user[3]}')
    print(f'Payment_type: {user[4]}')
    print('')
cursor.close()

