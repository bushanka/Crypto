import asyncio
import sqlite3

from aiogram import Bot
from aiogram.utils.exceptions import BotBlocked

from main import filter_param
from main import parse_all_info
import os

path_main_db = os.path.join(os.path.expanduser('~'), 'Crypto', 'main_settings', 'main_data.db')
path_settings_binance_garantex_db = os.path.join(os.path.expanduser('~'), 'Crypto', 'main_settings',
                                                 'settings_binance_garantex.db')

TOKEN = '1913516507:AAG7oDMX5EuIHo9FPwLhpx5bI6Bcja3Anx0'
CHAT_ID = -544855288

# Bot create
bot = Bot(token=TOKEN)


def sql_command(command_text, data_base_name='main_data.db', params=None):
    """Функция для отправки SQL запросов"""
    connection = False
    data = None
    try:
        connection = sqlite3.connect(data_base_name)
        cursor = connection.cursor()
        if params is None:
            cursor.execute(command_text)
            data = cursor.fetchall()
        else:
            cursor.execute(command_text, params)
            data = cursor.fetchall()
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if connection:
            connection.close()
    return data


async def send_info(user_id, texts_list_bin_gar, texts_list_gar_bin, texts_list_bz_gar):
    if len(texts_list_bin_gar) != 0:
        try:
            await bot.send_message(chat_id=user_id, text='\n\nBinance -> Garantex\n\n')
            for msg in texts_list_bin_gar:
                await bot.send_message(chat_id=user_id, text=msg)
        except BotBlocked:
            pass
    if len(texts_list_gar_bin) != 0:
        try:
            await bot.send_message(chat_id=user_id, text='\n\nGarantex -> Binance\n\n')
            for msg in texts_list_gar_bin:
                await bot.send_message(chat_id=user_id, text=msg)
        except BotBlocked:
            pass
    if len(texts_list_bz_gar) != 0:
        try:
            await bot.send_message(chat_id=user_id, text='\n\nBitzlato -> Garantex\n\n')
            for msg in texts_list_bz_gar:
                await bot.send_message(chat_id=user_id, text=msg)
        except BotBlocked:
            pass


async def start():
    while True:
        b, g, bz = parse_all_info()

        is_user_sub = sql_command("""SELECT subscriber_binance_garantex from main_users_data""", path_main_db)
        records_list = sql_command("""SELECT * from settings_binance_garantex""", path_settings_binance_garantex_db)

        coros_1 = []
        for iterate, user in enumerate(records_list):
            if is_user_sub[iterate][0] == 1:
                bin_gar_info, gar_bin_info, bz_gar_info = filter_param(volume=float(user[2]),
                                                                       payment_method={'Tinkoff': user[3],
                                                                                       'Sberbank': user[4]},
                                                                       parsed_gar=g,
                                                                       parsed_binance=b, parsed_bz=bz, percent=user[5],
                                                                       min_amount=user[6], is_binance_usdt=user[7],
                                                                       is_binance_eth=user[8], is_binance_btc=user[9],
                                                                       is_gar_usdt=user[10], is_gar_eth=user[11],
                                                                       is_gar_btc=user[12], is_bz_usdt=user[13],
                                                                       is_bz_eth=user[14], is_bz_btc=user[15])
                coros_1.append(
                    send_info(user_id=user[0], texts_list_bin_gar=bin_gar_info, texts_list_gar_bin=gar_bin_info,
                              texts_list_bz_gar=bz_gar_info))
        await asyncio.gather(*coros_1)
        await asyncio.sleep(60)

        # if float(parse_rub()) < 1.00:
        #     await bot.send_message(chat_id=CHAT_ID, text='BINANCE\n\nМожно купить баланс биржы 1 ₽ за 0.99 ₽')
        # await bot.send_message(chat_id=CHAT_ID, text='______________________________')
        # await asyncio.sleep(60)


if __name__ == '__main__':
    asyncio.run(start())
