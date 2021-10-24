import asyncio
import sqlite3

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher

from main import filter_param
from main import parse_all_info

TOKEN = '1913516507:AAG7oDMX5EuIHo9FPwLhpx5bI6Bcja3Anx0'
CHAT_ID = -544855288

# Bot create
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


def read_sqlite_table():
    try:
        sqlite_connection = sqlite3.connect('data.db')
        cursor = sqlite_connection.cursor()
        # print("Подключен к SQLite")

        sqlite_select_query = """SELECT * from users_data"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        cursor.close()
        return records

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


async def send_info(user_id, texts_list_bin_gar, texts_list_gar_bin, texts_list_bz_gar):
    if len(texts_list_bin_gar) != 0:
        await bot.send_message(chat_id=user_id, text='\n\nBinance -> Garantex\n\n')
        for msg in texts_list_bin_gar:
            await bot.send_message(chat_id=user_id, text=msg)
            # await bot.send_message(chat_id=user_id, text='\n\n______________\n\n')
    if len(texts_list_gar_bin) != 0:
        await bot.send_message(chat_id=user_id, text='\n\nGarantex -> Binance\n\n')
        for msg in texts_list_gar_bin:
            await bot.send_message(chat_id=user_id, text=msg)
    if len(texts_list_bz_gar) != 0:
        await bot.send_message(chat_id=user_id, text='\n\nBitzlato -> Garantex\n\n')
        for msg in texts_list_bz_gar:
            await bot.send_message(chat_id=user_id, text=msg)
    # if len(my_position) != 0:
    #     await bot.send_message(chat_id=user_id, text=my_position)
    #        await bot.send_message(chat_id=user_id, text='\n\n_________________________\n\n')


async def start():
    while True:
        b, g, bz = parse_all_info()
        records_list = read_sqlite_table()
        for user in records_list:
            if user[2] == 1:
                bin_gar_info, gar_bin_info, bz_gar_info = filter_param(volume=float(user[3]), payment_method=user[4],
                                                                       parsed_gar=g,
                                                                       parsed_binance=b, parsed_bz=bz, percent=user[8],
                                                                       min_amount=user[9], is_binance_usdt=user[10], is_binance_eth=user[11], is_binance_btc=user[12],
                                                                       is_gar_usdt=user[13], is_gar_eth=user[14], is_gar_btc=user[15], is_bz_usdt=user[16], is_bz_eth=user[17], is_bz_btc=user[18])
                try:
                    await send_info(user_id=user[0], texts_list_bin_gar=bin_gar_info, texts_list_gar_bin=gar_bin_info,
                                    texts_list_bz_gar=bz_gar_info)
                except:
                    pass
        await asyncio.sleep(120)

        # if float(parse_rub()) < 1.00:
        #     await bot.send_message(chat_id=CHAT_ID, text='BINANCE\n\nМожно купить баланс биржы 1 ₽ за 0.99 ₽')
        # await bot.send_message(chat_id=CHAT_ID, text='______________________________')
        # await asyncio.sleep(60)


if __name__ == '__main__':
    # executor.start_polling(dp)
    asyncio.run(start())
