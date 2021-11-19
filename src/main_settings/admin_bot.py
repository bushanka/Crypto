import sqlite3

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
import os
from admin_states import Cases

bot = Bot(token='2111176226:AAGGXMqDKARkFpRDkgbT6pj88HhONrh1-_w')
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

MY_ID = 383367365

# path_main_db = os.path.join(os.path.expanduser('D:\\'), 'MyDesctopFiles', 'business', 'CryptoBot', 'Crypto', 'src',
#                             'main_settings', 'main_data.db')


path_main_db = os.path.join(os.path.expanduser('~'), 'Crypto', 'src', 'main_settings', 'main_data.db')


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


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """Функция запуска бота. """
    is_my_id = message.chat.id
    if is_my_id == MY_ID:
        await bot.send_message(chat_id=MY_ID,
                               text="Ready")
    else:
        pass


@dp.message_handler(commands=['get_usr_info'])
async def start_command(message: types.Message):
    """Отображение всех пользователей"""
    is_my_id = message.chat.id
    if is_my_id == MY_ID:
        data = sql_command("""SELECT * FROM main_users_data""", data_base_name=path_main_db)
        for user_info in data:
            send_msg = '___________________________________\n\n' \
                       + f'ID: {user_info[0]}\n\n' + f'Nick: {user_info[1]}\n\n' \
                       + f'Is Subscruber Bin Gar: {user_info[2]}\n\n' \
                       + f'Time Subscribed: {user_info[3]}\n\n' \
                       + f'Is test access: {user_info[4]}\n\n'\
                       + f'Is Subscruber Bestch Bin: {user_info[5]}\n\n' \
                       + f'Time Subscribed: {user_info[6]}\n\n' \
                       + f'Is test access: {user_info[7]}\n\n'\
                       + '___________________________________'

            await bot.send_message(chat_id=MY_ID, text=send_msg)
    else:
        pass


@dp.message_handler(commands=['time_bin_gar_bz'])
async def start_command(message: types.Message):
    """Отображение всех пользователей"""
    is_my_id = message.chat.id
    if is_my_id == MY_ID:
        await bot.send_message(chat_id=MY_ID, text='Ok. Send me info: userid,time')
        await Cases.STATE_CHANGE_TIME_BIN_GAR_BZ.set()
    else:
        pass


@dp.message_handler(state=Cases.STATE_CHANGE_TIME_BIN_GAR_BZ)
async def settings(message: types.Message, state: FSMContext):
    list_msg = message.text.split(',')
    msg_userid, msg_usertime = list_msg[0], list_msg[1]
    try:
        sql_command("""UPDATE main_users_data SET time_subscribe_binance_garantex = ? WHERE userid = ?;""",
                    params=(msg_usertime, int(msg_userid)), data_base_name=path_main_db)
        await bot.send_message(chat_id=MY_ID, text='Success')
        await state.reset_state()

    except:
        await bot.send_message(chat_id=MY_ID, text='Error!\nTry again')


@dp.message_handler(commands=['unsubscribe_bin_gar_bz'])
async def start_command(message: types.Message):
    """Отображение всех пользователей"""
    is_my_id = message.chat.id
    if is_my_id == MY_ID:
        await bot.send_message(chat_id=MY_ID, text='Ok. Send me userid to unsubscribe')
        await Cases.STATE_UNSUBSCRIBE_BIN_GAR_BZ.set()
    else:
        pass


@dp.message_handler(state=Cases.STATE_UNSUBSCRIBE_BIN_GAR_BZ)
async def settings(message: types.Message, state: FSMContext):
    msg_userid = message.text
    try:
        sql_command("""UPDATE main_users_data SET subscriber_binance_garantex = ? WHERE userid = ?;""",
                    params=(0, int(msg_userid)), data_base_name=path_main_db)
        await bot.send_message(chat_id=MY_ID, text='Success')
        await state.reset_state()
    except:
        await bot.send_message(chat_id=MY_ID, text='Error!\nTry again')


@dp.message_handler(commands=['subscribe_bin_gar_bz'])
async def start_command(message: types.Message):
    """Отображение всех пользователей"""
    is_my_id = message.chat.id
    if is_my_id == MY_ID:
        await bot.send_message(chat_id=MY_ID, text='Ok. Send me userid to subscribe')
        await Cases.STATE_SUBSCRIBE_BIN_GAR_BZ.set()
    else:
        pass


@dp.message_handler(state=Cases.STATE_SUBSCRIBE_BIN_GAR_BZ)
async def settings(message: types.Message, state: FSMContext):
    msg_userid = message.text
    try:
        sql_command("""UPDATE main_users_data SET subscriber_binance_garantex = ? WHERE userid = ?;""",
                    params=(1, int(msg_userid)), data_base_name=path_main_db)
        await bot.send_message(chat_id=MY_ID, text='Success')
        await state.reset_state()
    except:
        await bot.send_message(chat_id=MY_ID, text='Error!\nTry again')


@dp.message_handler(commands=['time_bch_bin'])
async def start_command(message: types.Message):
    """Отображение всех пользователей"""
    is_my_id = message.chat.id
    if is_my_id == MY_ID:
        await bot.send_message(chat_id=MY_ID, text='Ok. Send me info: userid,time')
        await Cases.STATE_CHANGE_TIME_BCH_BIN.set()
    else:
        pass


@dp.message_handler(state=Cases.STATE_CHANGE_TIME_BCH_BIN)
async def settings(message: types.Message, state: FSMContext):
    list_msg = message.text.split(',')
    msg_userid, msg_usertime = list_msg[0], list_msg[1]
    try:
        sql_command("""UPDATE main_users_data SET time_subscribe_bestchange_binance = ? WHERE userid = ?;""",
                    params=(msg_usertime, int(msg_userid)), data_base_name=path_main_db)
        await bot.send_message(chat_id=MY_ID, text='Success')
        await state.reset_state()

    except:
        await bot.send_message(chat_id=MY_ID, text='Error!\nTry again')


@dp.message_handler(commands=['unsubscribe_bch_bin'])
async def start_command(message: types.Message):
    """Отображение всех пользователей"""
    is_my_id = message.chat.id
    if is_my_id == MY_ID:
        await bot.send_message(chat_id=MY_ID, text='Ok. Send me userid to unsubscribe')
        await Cases.STATE_UNSUBSCRIBE_BCH_BIN.set()
    else:
        pass


@dp.message_handler(state=Cases.STATE_UNSUBSCRIBE_BCH_BIN)
async def settings(message: types.Message, state: FSMContext):
    msg_userid = message.text
    try:
        sql_command("""UPDATE main_users_data SET subscriber_bestchange_binance = ? WHERE userid = ?;""",
                    params=(0, int(msg_userid)), data_base_name=path_main_db)
        await bot.send_message(chat_id=MY_ID, text='Success')
        await state.reset_state()
    except:
        await bot.send_message(chat_id=MY_ID, text='Error!\nTry again')


@dp.message_handler(commands=['subscribe_bch_bin'])
async def start_command(message: types.Message):
    """Отображение всех пользователей"""
    is_my_id = message.chat.id
    if is_my_id == MY_ID:
        await bot.send_message(chat_id=MY_ID, text='Ok. Send me userid to subscribe')
        await Cases.STATE_SUBSCRIBE_BCH_BIN.set()
    else:
        pass


@dp.message_handler(state=Cases.STATE_SUBSCRIBE_BCH_BIN)
async def settings(message: types.Message, state: FSMContext):
    msg_userid = message.text
    try:
        sql_command("""UPDATE main_users_data SET subscriber_bestchange_binance = ? WHERE userid = ?;""",
                    params=(1, int(msg_userid)), data_base_name=path_main_db)
        await bot.send_message(chat_id=MY_ID, text='Success')
        await state.reset_state()
    except:
        await bot.send_message(chat_id=MY_ID, text='Error!\nTry again')


if __name__ == '__main__':
    executor.start_polling(dp)
