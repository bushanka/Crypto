import asyncio
# import sqlite3

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram import types

from bch_bin_backend import start_parse_bch
from time import sleep as freezee

TOKEN = '2099296853:AAG1zzSwoz6AIae1km-5WTmYJDGan6yIRFM'
CHAT_ID = -1001582710312

#TEST_ONLY
#TOKEN = '2057297662:AAGS5TUhqcS3d1-QObWrO6CITLnDtDXp8p0'
#CHAT_ID = -636744268

# Bot create
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


# def read_sqlite_table():
#     try:
#         sqlite_connection = sqlite3.connect('data.db')
#         cursor = sqlite_connection.cursor()
#         # print("Подключен к SQLite")
#
#         sqlite_select_query = """SELECT * from users_data"""
#         cursor.execute(sqlite_select_query)
#         records = cursor.fetchall()
#         cursor.close()
#         return records
#
#     except sqlite3.Error as error:
#         print("Ошибка при работе с SQLite", error)


async def send_info(user_id, msg):
    for mes in msg[0][:10]:
        await bot.send_message(chat_id=CHAT_ID, text=mes, parse_mode=types.ParseMode.HTML)
        freezee(1)
    for mes in msg[1][:10]:
        await bot.send_message(chat_id=CHAT_ID, text=mes, parse_mode=types.ParseMode.HTML)
        freezee(1)

    await bot.send_message(chat_id=383367365, text='Bot is working normal')


async def start():
    while True:
        data = 383367365
        text = start_parse_bch()
        await send_info(user_id=data, msg=text)
        await asyncio.sleep(60)


if __name__ == '__main__':
    asyncio.run(start())
