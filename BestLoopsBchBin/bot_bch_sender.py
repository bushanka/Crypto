import asyncio
import sqlite3

from aiogram import Bot
from aiogram import types

from bch_bin_backend import start_parse_bch, filter_params
# from time import sleep as freezee
import os

TOKEN_QIWI = '2082105080:AAFdAAjb6eWlGqKQ_Gx__2dafmZ0WXbJGGY'
TOKEN_Cards = '2031184361:AAHjrpu0Z4N9txyGnM6HzYXKYu-4s7MB7iM'
TOKEN_NoCards = '2066398775:AAFIvY2l4xZ2d7iaJ4lVo2GdP_qcMHE3vDE'

# Bot create
bot_qiwi = Bot(token=TOKEN_QIWI)
bot_cards = Bot(token=TOKEN_Cards)
bot_nocards = Bot(token=TOKEN_NoCards)

# path_main_db = os.path.join(os.path.expanduser('D:\\'), 'MyDesctopFiles', 'business', 'Crypto_bot', 'Crypto',
#                             'main_settings', 'main_data.db')
# path_settings_bestchange_binance_db = os.path.join(os.path.expanduser('D:\\'), 'MyDesctopFiles', 'business',
#                                                    'Crypto_bot',
#                                                    'Crypto',
#                                                    'main_settings', 'settings_bestchange_binance.db')

path_main_db = os.path.join(os.path.expanduser('~'), 'Crypto', 'main_settings', 'main_data.db')
path_settings_bestchange_binance_db = os.path.join(os.path.expanduser('~'), 'Crypto', 'main_settings',
                                                   'settings_bestchange_binance.db')


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


async def send_info(user_id, msg):
    for mes in msg[0][:5]:
        if mes['Paymethod'] == 0:  # QIWI
            try:
                await bot_qiwi.send_message(chat_id=user_id, text=mes['Text'], parse_mode=types.ParseMode.HTML)
            except:
                pass
        if mes['Paymethod'] == 1:  # CARDS
            try:
                await bot_cards.send_message(chat_id=user_id, text=mes['Text'], parse_mode=types.ParseMode.HTML)
            except:
                pass
    for mes in msg[1][:5]:
        if mes['Paymethod'] == 0:  # QIWI
            try:
                await bot_qiwi.send_message(chat_id=user_id, text=mes['Text'], parse_mode=types.ParseMode.HTML)
            except:
                pass
        if mes['Paymethod'] == 1:  # CARDS
            try:
                await bot_cards.send_message(chat_id=user_id, text=mes['Text'], parse_mode=types.ParseMode.HTML)
            except:
                pass

    # await bot.send_message(chat_id=383367365, text='Bot is working normal')


async def start():
    # import time
    while True:
        is_user_sub = sql_command("""SELECT subscriber_bestchange_binance from main_users_data""", path_main_db)
        records_list = sql_command("""SELECT * from settings_bestchange_binance""", path_settings_bestchange_binance_db)
        text = start_parse_bch()
        # start_time = time.time()
        for iterate, user in enumerate(records_list):
            if is_user_sub[iterate][0] == 1:
                filtered_text = filter_params(user[2], text[0], text[1])
                await send_info(user_id=user[0], msg=filtered_text)
        # print("--- %s seconds to send ---" % (time.time() - start_time))
        await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(start())
