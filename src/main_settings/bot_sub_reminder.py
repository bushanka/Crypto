import asyncio
import sqlite3
from datetime import date
from datetime import datetime as dtmp
from datetime import timedelta
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
import os

path_main_db = os.path.join(os.path.expanduser('~'), 'Crypto', 'src',
                            'main_settings', 'main_data.db')

bot = Bot(token='1971360278:AAEmqzP0fKTi2a_eaNcMMLn0386ouLuwIT0')
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


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


async def start():
    while True:
        today = date.today()
        subs_data = sql_command("""SELECT * FROM main_users_data""", path_main_db)
        for user in subs_data:
            #   ______Проверяем время начала подписки______
            # ______Отписываем если прошло больше 30 дней______
           # print(today - dtmp.strptime(user[3], '%Y-%m-%d').date())
            if user[2] != 0 and (user[3] is not None and user[3] != 'None'):  # Binance-Garantex_BestChange Scheme
                delta = today - dtmp.strptime(user[3].strip(), '%Y-%m-%d').date()
                if delta >= timedelta(days=30, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
                    sql_command("""UPDATE main_users_data SET subscriber_binance_garantex = ? WHERE userid = ?;""",
                                params=(0, user[0]), data_base_name=path_main_db)
                    try:
                        await bot.send_message(chat_id=user[0],
                                               text="Подписка на схему Binance-Garantex-BestChange закончилась"
                                                    "\n\nДля оплаты перейдите в главное меню и выберете "
                                                    "оплатить подписку")
                    except:
                        pass

            if user[5] != 0 and (user[6] is not None and user[6] != 'None'):
                # BestChange_Binance Scheme
                print(user[6] is not None)
                delta = today - dtmp.strptime(user[6].strip(), '%Y-%m-%d').date()
                if delta >= timedelta(days=30, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
                    sql_command("""UPDATE main_users_data SET subscriber_bestchange_binance = ? WHERE userid = ?;""",
                                params=(0, user[0]), data_base_name=path_main_db)
                    try:
                        await bot.send_message(chat_id=user[0],
                                               text="Подписка на схему BestChange-Binance закончилась"
                                                    "\n\nДля оплаты перейдите в главное меню и выберете "
                                                    "оплатить подписку")
                    except:
                        pass

            if user[8] != 0 and (user[9] is not None and user[9] != 'None'):  # Garantex_BestChange Scheme
                delta = today - dtmp.strptime(user[9].strip(), '%Y-%m-%d').date()
                if delta >= timedelta(days=30, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
                    sql_command("""UPDATE main_users_data SET subscriber_bestchange_garantex = ? WHERE userid = ?;""",
                                params=(0, user[0]), data_base_name=path_main_db)
                    try:
                        await bot.send_message(chat_id=user[0],
                                               text="Подписка на схему Garantex-BestChange закончилась"
                                                    "\n\nДля оплаты перейдите в главное меню и выберете "
                                                    "оплатить подписку")
                    except:
                        pass

            #   ______Проверяем время начала подписки______
            # ______Высылаем сообщение что подписка скоро кончится______
            if user[2] != 0 and (user[3] is not None and user[3] != 'None'):
                delta = today - dtmp.strptime(user[3].strip(), '%Y-%m-%d').date()
                if timedelta(days=29, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0,
                             weeks=0) <= delta < timedelta(days=30, seconds=0, microseconds=0, milliseconds=0,
                                                           minutes=0,
                                                           hours=0,
                                                           weeks=0):
                    try:
                        await bot.send_message(chat_id=user[0],
                                               text="Подписка на схему Binance-Garantex-Bitzlato закончится завтра"
                                                    "\n\nДля оплаты перейдите в главное меню и выберете "
                                                    "оплатить подписку")
                    except:
                        pass
            if user[5] != 0 and (user[6] is not None and user[6] != 'None'):
                delta = today - dtmp.strptime(user[6].strip(), '%Y-%m-%d').date()
                if timedelta(days=29, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0,
                             weeks=0) <= delta < timedelta(days=30, seconds=0, microseconds=0, milliseconds=0,
                                                           minutes=0,
                                                           hours=0,
                                                           weeks=0):
                    try:
                        await bot.send_message(chat_id=user[0],
                                               text="Подписка на схему BestChange-Binance закончится завтра"
                                                    "\n\nДля оплаты перейдите в главное меню и выберете "
                                                    "оплатить подписку")
                    except:
                        pass
            if user[8] != 0 and (user[9] is not None and user[9] != 'None'):
                delta = today - dtmp.strptime(user[9].strip(), '%Y-%m-%d').date()
                if timedelta(days=29, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0,
                             weeks=0) <= delta < timedelta(days=30, seconds=0, microseconds=0, milliseconds=0,
                                                           minutes=0,
                                                           hours=0,
                                                           weeks=0):
                    try:
                        await bot.send_message(chat_id=user[0],
                                               text="Подписка на схему BestChange-Garantex закончится завтра"
                                                    "\n\nДля оплаты перейдите в главное меню и выберете "
                                                    "оплатить подписку")
                    except:
                        pass
        await asyncio.sleep(24 * 60 * 60)


if __name__ == '__main__':
    asyncio.run(start())
