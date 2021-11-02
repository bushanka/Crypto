import sqlite3

sqlite_connection = sqlite3.connect('data.db')
cursor = sqlite_connection.cursor()


cursor.execute("""ALTER TABLE users_data ADD COLUMN is_bz_usdt INTEGER DEFAULT 1;""")
cursor.execute("""ALTER TABLE users_data ADD COLUMN is_bz_eth INTEGER DEFAULT 1;""")
cursor.execute("""ALTER TABLE users_data ADD COLUMN is_bz_btc INTEGER DEFAULT 1;""")

sqlite_connection.commit()
cursor.close()
