import asyncio
import sqlite3
from aiogram import Bot
from aiogram import types
from time import sleep as freezee
from bch_bin_backend import parse_all_from_bch, filter_params
from aiogram.utils.exceptions import BotBlocked, ChatNotFound,  RetryAfter
import os

TOKEN_QIWI = '2082105080:AAFdAAjb6eWlGqKQ_Gx__2dafmZ0WXbJGGY'
TOKEN_Cards = '2031184361:AAHjrpu0Z4N9txyGnM6HzYXKYu-4s7MB7iM'
TOKEN_NoCards = '2066398775:AAFIvY2l4xZ2d7iaJ4lVo2GdP_qcMHE3vDE'

# DELETE AFTER ALL USERS COME TO NEW VERSION
TOKEN = '2099296853:AAG1zzSwoz6AIae1km-5WTmYJDGan6yIRFM'
CHAT_ID = -1001582710312
# TEST ONLY
# TOKEN = '2057297662:AAGS5TUhqcS3d1-QObWrO6CITLnDtDXp8p0'
# CHAT_ID = -636744268
# ________________________________

# Bot create
bot_qiwi = Bot(token=TOKEN_QIWI)
bot_cards = Bot(token=TOKEN_Cards)
bot_nocards = Bot(token=TOKEN_NoCards)
#bot = Bot(token=TOKEN)
# path_main_db = os.path.join(os.path.expanduser('D:\\'), 'MyDesctopFiles', 'business', 'Crypto_bot', 'Crypto', 'src',
#                             'main_settings', 'main_data.db')
# path_settings_bestchange_binance_db = os.path.join(os.path.expanduser('D:\\'), 'MyDesctopFiles', 'business',
#                                                    'Crypto_bot',
#                                                    'Crypto', 'src',
#                                                    'main_settings', 'settings_bestchange_binance.db')


path_main_db = os.path.join(os.path.expanduser('~'), 'Crypto','src', 'main_settings', 'main_data.db')
path_settings_bestchange_binance_db = os.path.join(os.path.expanduser('~'), 'Crypto','src', 'main_settings',
                                                   'settings_bestchange_binance.db')
#headers = requests.utils.default_headers()
#headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

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


async def send_info_legacy(msg):
    # DELETE AFTER ALL USERS CHANGE VERSION
    for mes in msg[0][:10]:
        await bot.send_message(chat_id=CHAT_ID, text=mes['Text'], parse_mode=types.ParseMode.HTML)
        freezee(1)
    for mes in msg[1][:10]:
        await bot.send_message(chat_id=CHAT_ID, text=mes['Text'], parse_mode=types.ParseMode.HTML)
        freezee(1)
    await bot.send_message(chat_id=383367365, text='Bot is working normal')


# _______________________________________


async def send_info_legacy_2(user_id, msg):
    #user_id = 383367365
    for mes in msg[0][:5]:
        if mes['Paymethod'] == 0:  # QIWI
            try:
                await bot_qiwi.send_message(chat_id=user_id, text=mes['Text'], parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound):
                pass
        if mes['Paymethod'] == 1:  # CARDS
            try:
                await bot_cards.send_message(chat_id=user_id, text=mes['Text'], parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound):
                pass
        if mes['Paymethod'] == 2:  # NO CARDS
            try:
                await bot_nocards.send_message(chat_id=user_id, text=mes['Text'], parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound):
                pass
    for mes in msg[1][:5]:
        if mes['Paymethod'] == 0:  # QIWI
            try:
                await bot_qiwi.send_message(chat_id=user_id, text=mes['Text'], parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound):
                pass
        if mes['Paymethod'] == 1:  # CARDS
            try:
                await bot_cards.send_message(chat_id=user_id, text=mes['Text'], parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound):
                pass
        if mes['Paymethod'] == 2:  # NO CARDS
            try:
                await bot_nocards.send_message(chat_id=user_id, text=mes['Text'], parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound):
                pass

async def send_info(user_id, msg):
    # user_id = 383367365
    message_a_qiwi = []
    message_a_cards = []
    message_a_nocards = []
    message_b_qiwi = []
    message_b_cards = []
    message_b_nocards = []
    for mes in msg[0]:
        if mes['Paymethod'] == 0:  # QIWI
            message_a_qiwi.append(mes['Text'])
        elif mes['Paymethod'] == 1:  # CARDS
            message_a_cards.append(mes['Text'])
        else:  # NO CARDS
            message_a_nocards.append(mes['Text'])

    for mes in msg[1]:
        if mes['Paymethod'] == 0:  # QIWI
            message_b_qiwi.append(mes['Text'])
        elif mes['Paymethod'] == 1:  # CARDS
            message_b_cards.append(mes['Text'])
        else:  # NO CARDS
            message_b_nocards.append(mes['Text'])
    if type(user_id) != list:
        for send_inf in message_a_qiwi[:3]:
            try:
                await bot_qiwi.send_message(chat_id=user_id, text=send_inf, parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound, RetryAfter):
                pass
        for send_inf in message_a_cards[:3]:
            try:
                await bot_cards.send_message(chat_id=user_id, text=send_inf, parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound, RetryAfter):
                pass
        for send_inf in message_a_nocards[:3]:
            try:
                await bot_nocards.send_message(chat_id=user_id, text=send_inf, parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound, RetryAfter):
                pass

        for send_inf in message_b_qiwi[:3]:
            try:
                await bot_qiwi.send_message(chat_id=user_id, text=send_inf, parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound, RetryAfter):
                pass
        for send_inf in message_b_cards[:3]:
            try:
                await bot_cards.send_message(chat_id=user_id, text=send_inf, parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound, RetryAfter):
                pass
        for send_inf in message_b_nocards[:3]:
            try:
                await bot_nocards.send_message(chat_id=user_id, text=send_inf, parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound, RetryAfter):
                pass
    else:
        for send_inf in message_a_qiwi[:3]:
            try:
                await bot_qiwi.send_message(chat_id=-1001603600103, text=send_inf, parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound, RetryAfter):
                pass
            await asyncio.sleep(1)
        for send_inf in message_a_cards[:3]:
            try:
                await bot_cards.send_message(chat_id=-1001647983723, text=send_inf, parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound, RetryAfter):
                pass
            await asyncio.sleep(1)
        for send_inf in message_a_nocards[:3]:
            try:
                await bot_nocards.send_message(chat_id=-1001631290076, text=send_inf, parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound, RetryAfter):
                pass
            await asyncio.sleep(1)

        for send_inf in message_b_qiwi[:3]:
            try:
                await bot_qiwi.send_message(chat_id=-1001603600103, text=send_inf, parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound, RetryAfter):
                pass
            await asyncio.sleep(1)
        for send_inf in message_b_cards[:3]:
            try:
                await bot_cards.send_message(chat_id=-1001647983723, text=send_inf, parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound, RetryAfter):
                pass
            await asyncio.sleep(1)
        for send_inf in message_b_nocards[:3]:
            try:
                await bot_nocards.send_message(chat_id=-1001631290076, text=send_inf, parse_mode=types.ParseMode.HTML)
            except (BotBlocked, ChatNotFound, RetryAfter):
                pass
            await asyncio.sleep(1)




async def start():
    while True:
        is_user_sub = sql_command("""SELECT subscriber_bestchange_binance from main_users_data""", path_main_db)
        records_list = sql_command("""SELECT * from settings_bestchange_binance""", path_settings_bestchange_binance_db)

        text = parse_all_from_bch()
        await send_info([], msg=filter_params(0.5, text[0], text[1]))

        coros_1 = []
        for iterate, user in enumerate(records_list):
            if is_user_sub[iterate][0] == 1:
                coros_1.append(send_info(user_id=user[0], msg=filter_params(user[2], text[0], text[1])))  # user[2]

        await asyncio.gather(*coros_1)

        await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(start())
