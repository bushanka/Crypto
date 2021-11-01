import sqlite3

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

from states import Cases

# bot = Bot(token='1023131676:AAFLtJwB8vawUY3DHibc4LpWl_wltZvbE0U') # TEST ONLY
bot = Bot(token='1971360278:AAEmqzP0fKTi2a_eaNcMMLn0386ouLuwIT0')
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

button_settings = KeyboardButton('Настройки ⚙')
button_subscribe = KeyboardButton('Оплата подписки 💵')
button_help = KeyboardButton('Помощь 🚑')
button_back = KeyboardButton('Назад')

inline_btn_settings = InlineKeyboardButton('Настройки ⚙', callback_data='button_settings')
inline_btn_subscribe = InlineKeyboardButton('Оплата подписки 💵', callback_data='button_subscribe')
inline_btn_help = InlineKeyboardButton('Помощь 🚑', callback_data='button_help')
inline_btn_back = InlineKeyboardButton('Назад', callback_data='button_back')
inline_btn_back_main = InlineKeyboardButton('Назад', callback_data='button_back_main')

inline_main_kb = InlineKeyboardMarkup().add(inline_btn_settings, inline_btn_subscribe, inline_btn_help)
inline_back_main_kb = InlineKeyboardMarkup().add(inline_btn_back_main)

button_settings_binance_garantex = InlineKeyboardButton('Binance-Garantex-Bitzlato',
                                                        callback_data='button_settings_bin_gar')
button_settings_bestchange_binance = InlineKeyboardButton('Bestchange-Binance',
                                                          callback_data='button_settings_bch_gin')
button_settings_bestchange_garantex = InlineKeyboardButton('Bestchange-Garantex',
                                                           callback_data='button_settings_bch_gar')

inline_button_exchanges_settings = InlineKeyboardButton('Биржи', callback_data='button_exchanges_settings')
inline_button_trade_settings = InlineKeyboardButton('Торговля', callback_data='button_trade_settings')
inline_button_back_bot_settings = InlineKeyboardButton('Назад', callback_data='button_back_bot_settings')
inline_binance_garantex_settings_kb = InlineKeyboardMarkup().add(inline_button_exchanges_settings,
                                                                 inline_button_trade_settings,
                                                                 inline_button_back_bot_settings)

inline_button_upper_limit = InlineKeyboardButton('Верхний лимит', callback_data='button_upper_limit')
inline_button_down_limits = InlineKeyboardButton('Нижний лимит', callback_data='button_down_limit')
inline_button_bingar_percent = InlineKeyboardButton('Процент', callback_data='button_bingar_percent')
inline_button_bingar_paymeth = InlineKeyboardButton('Карты', callback_data='button_bingar_paymeth')
inline_button_back_bingar = InlineKeyboardButton('Назад', callback_data='button_back_bingar')

inline_button_bingar_tink_yes = InlineKeyboardButton('Тинькофф ✔', callback_data='button_tink_bin_gar_yes')
inline_button_bingar_sber_yes = InlineKeyboardButton('Сбербанкк ✔', callback_data='button_sber_bin_gar_yes')
inline_button_bingar_tink_no = InlineKeyboardButton('Тинькофф ❌', callback_data='button_tink_bin_gar_no')
inline_button_bingar_sber_no = InlineKeyboardButton('Сбербанкк ❌', callback_data='button_sber_bin_gar_no')

inline_trade_settings_kb = InlineKeyboardMarkup().add(inline_button_upper_limit, inline_button_down_limits,
                                                      inline_button_bingar_percent, inline_button_bingar_paymeth,
                                                      inline_button_back_bingar)

inline_button_binance_settings = InlineKeyboardButton('Binance', callback_data='button_binance_settings')
inline_button_garantex_settings = InlineKeyboardButton('Garantex', callback_data='button_garantex_settings')
inline_button_bitzlato_settings = InlineKeyboardButton('Bitzlato', callback_data='button_bitzlato_settings')

inline_button_bingar_bin_eth_no = InlineKeyboardButton('ETH ❌', callback_data='button_bingar_bin_eth_no')
inline_button_bingar_bin_eth_yes = InlineKeyboardButton('ETH ✔', callback_data='button_bingar_bin_eth_yes')
inline_button_bingar_bin_usdt_no = InlineKeyboardButton('USDT ❌', callback_data='button_bingar_bin_usdt_no')
inline_button_bingar_bin_usdt_yes = InlineKeyboardButton('USDT ✔', callback_data='button_bingar_bin_usdt_yes')
inline_button_bingar_bin_btc_no = InlineKeyboardButton('BTC ❌', callback_data='button_bingar_bin_btc_no')
inline_button_bingar_bin_btc_yes = InlineKeyboardButton('BTC ✔', callback_data='button_bingar_bin_btc_yes')

inline_button_bingar_gar_eth_no = InlineKeyboardButton('ETH ❌', callback_data='button_bingar_gar_eth_no')
inline_button_bingar_gar_eth_yes = InlineKeyboardButton('ETH ✔', callback_data='button_bingar_gar_eth_yes')
inline_button_bingar_gar_usdt_no = InlineKeyboardButton('USDT ❌', callback_data='button_bingar_gar_usdt_no')
inline_button_bingar_gar_usdt_yes = InlineKeyboardButton('USDT ✔', callback_data='button_bingar_gar_usdt_yes')
inline_button_bingar_gar_btc_no = InlineKeyboardButton('BTC ❌', callback_data='button_bingar_gar_btc_no')
inline_button_bingar_gar_btc_yes = InlineKeyboardButton('BTC ✔', callback_data='button_bingar_gar_btc_yes')

inline_button_bingar_bz_eth_no = InlineKeyboardButton('ETH ❌', callback_data='button_bingar_bz_eth_no')
inline_button_bingar_bz_eth_yes = InlineKeyboardButton('ETH ✔', callback_data='button_bingar_bz_eth_yes')
inline_button_bingar_bz_usdt_no = InlineKeyboardButton('USDT ❌', callback_data='button_bingar_bz_usdt_no')
inline_button_bingar_bz_usdt_yes = InlineKeyboardButton('USDT ✔', callback_data='button_bingar_bz_usdt_yes')
inline_button_bingar_bz_btc_no = InlineKeyboardButton('BTC ❌', callback_data='button_bingar_bz_btc_no')
inline_button_bingar_bz_btc_yes = InlineKeyboardButton('BTC ✔', callback_data='button_bingar_bz_btc_yes')

inline_button_bchbin_percent = InlineKeyboardButton('Процент', callback_data='button_bchbin_percent')
inline_button_beschange_binance_kb = InlineKeyboardMarkup().add(inline_button_bchbin_percent, inline_btn_back_main)

inline_button_exchange_kb = InlineKeyboardMarkup().add(inline_button_binance_settings, inline_button_garantex_settings,
                                                       inline_button_bitzlato_settings, inline_button_back_bingar)


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


# Создание баз данных если их нет
sql_command("""CREATE TABLE IF NOT EXISTS main_users_data(
"userid" INT PRIMARY KEY,
"username" TEXT,
"subscriber_binance_garantex" INTEGER DEFAULT 0,
"time_subscribe_binance_garantex" TEXT,
"test_access_binance_garantex" TEXT DEFAULT 'None',
"subscriber_bestchange_binance" INTEGER DEFAULT 0,
"time_subscribe_bestchange_binance" TEXT,
"test_access_bestchange_binance" TEXT DEFAULT 'None',
"subscriber_bestchange_garantex" INTEGER DEFAULT 0,
"time_subscribe_bestchange_garantex" TEXT,
"test_access_bestchange_garantex" TEXT DEFAULT 'None');""")

sql_command("""CREATE TABLE IF NOT EXISTS settings_binance_garantex(
"userid" INT PRIMARY KEY,
"username" TEXT,
"volume" TEXT DEFAULT 100000,
"payment_method_tinkoff" INTEGER DEFAULT 1,
"payment_method_sberbank" INTEGER DEFAULT 1,
"percent" REAL DEFAULT 0,
"min_amount" INTEGER DEFAULT 5000,
"is_binance_usdt" INTEGER DEFAULT 1,
"is_binance_eth" INTEGER DEFAULT 1,
"is_binance_btc" INTEGER DEFAULT 1,
"is_garantex_usdt" INTEGER DEFAULT 1,
"is_garantex_eth" INTEGER DEFAULT 1,
"is_garantex_btc" INTEGER DEFAULT 1,
"is_bz_usdt" INTEGER DEFAULT 1,
"is_bz_eth" INTEGER DEFAULT 1,
"is_bz_btc" INTEGER DEFAULT 1);""", data_base_name='settings_binance_garantex.db')

sql_command("""CREATE TABLE IF NOT EXISTS settings_bestchange_binance(
"userid" INT PRIMARY KEY,
"username" TEXT,
"percent" REAL DEFAULT 0);""", data_base_name='settings_bestchange_binance.db')

sql_command("""CREATE TABLE IF NOT EXISTS settings_bestchange_garantex(
"userid" INT PRIMARY KEY,
"username" TEXT,
"percent" REAL DEFAULT 0);""", data_base_name='settings_bestchange_garantex.db')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """Функция запуска бота. Записывает пользователя во все быз данных если его там нет"""
    message_user = (message.chat.id, message.chat.username)

    data_main = sql_command("SELECT userid FROM main_users_data WHERE userid = ?;", params=(message_user[0],))

    data_settings_binance_garantex = sql_command("SELECT userid FROM settings_binance_garantex WHERE userid = ?;",
                                                 params=(message_user[0],),
                                                 data_base_name='settings_binance_garantex.db')

    data_settings_bestchange_binance = sql_command(
        "SELECT userid FROM settings_bestchange_binance WHERE userid = ?;",
        params=(message_user[0],),
        data_base_name='settings_bestchange_binance.db')

    data_settings_bestchange_garantex = sql_command(
        "SELECT userid FROM settings_bestchange_garantex WHERE userid = ?;",
        params=(message_user[0],),
        data_base_name='settings_bestchange_garantex.db')

    if len(data_main) == 0:
        sql_command("""INSERT INTO main_users_data(userid, username) VALUES(?,?);""", params=message_user)

    if len(data_settings_binance_garantex) == 0:
        sql_command("""INSERT INTO settings_binance_garantex(userid, username) VALUES(?,?);""", params=message_user,
                    data_base_name='settings_binance_garantex.db')

    if len(data_settings_bestchange_binance) == 0:
        sql_command("""INSERT INTO settings_bestchange_binance(userid, username) VALUES(?,?);""", params=message_user,
                    data_base_name='settings_bestchange_binance.db')

    if len(data_settings_bestchange_garantex) == 0:
        sql_command("""INSERT INTO settings_bestchange_garantex(userid, username) VALUES(?,?);""", params=message_user,
                    data_base_name='settings_bestchange_garantex.db')

    await message.reply(
        "В этом боте находится твой аккаунт\n\n"
        "Для пробного доступа напиши @e_usovchan",
        reply_markup=inline_main_kb, reply=False)


@dp.callback_query_handler(lambda c: c.data == 'button_help')
async def process_callback_button1(callback_query: types.CallbackQuery):
    """Кнопка помощи"""
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text='По всем вопросам\nпишите сюда 👉 @e_usovchan',
                                reply_markup=inline_back_main_kb)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == 'button_back_main' or c.data == 'button_back')
async def process_callback_button1(callback_query: types.CallbackQuery):
    """Кнопка возврата в главное меню"""
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text="В этом боте находится твой аккаунт\n\nДля пробного доступа напиши @e_usovchan",
                                reply_markup=inline_main_kb)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == 'button_subscribe')
async def process_callback_button1(callback_query: types.CallbackQuery):
    """Кнопка оплаты подписки"""
    subscriber_id = str(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text="Чтобы продлить подписку на месяц, переведите 49 USDT на один из адресов: "
                                     "\n\nBSC(BEP20):\n0x93f5e1069a1cd94c4166c5060b770563fbba12de\n\nTron(TRC20):"
                                     "\nTE8FdD1RWiBvMsEMdtk5FJwvDQBF2vt7Ai\n\nИспользуйте биржу Binance чтобы платить "
                                     "без комиссии!\n\nПосле оплаты напишите @e_usovchan\nв сообщении укажите "
                                     "\n1. Какую схему оплатили"
                                     " \n2. Ваш ID: " + subscriber_id,
                                reply_markup=inline_back_main_kb)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == 'button_settings' or c.data == 'button_back_bot_settings')
async def process_callback_button1(callback_query: types.CallbackQuery):
    """Кнопка настроек связок"""
    message_user_id = callback_query.from_user.id

    inline_settings_kb = InlineKeyboardMarkup(row_width=1)

    is_binance_garantex = sql_command(
        "SELECT subscriber_binance_garantex FROM main_users_data WHERE userid = ?;", params=(message_user_id,),
        data_base_name='main_data.db')

    is_bestchange_binance = sql_command(
        "SELECT subscriber_bestchange_binance FROM main_users_data WHERE userid = ?;", params=(message_user_id,),
        data_base_name='main_data.db')

    is_bestchange_garantex = sql_command(
        "SELECT subscriber_bestchange_garantex FROM main_users_data WHERE userid = ?;", params=(message_user_id,),
        data_base_name='main_data.db')

    if is_binance_garantex[0][0]:
        inline_settings_kb.add(button_settings_binance_garantex)
    if is_bestchange_binance[0][0]:
        inline_settings_kb.add(button_settings_bestchange_binance)
    if is_bestchange_garantex[0][0]:
        inline_settings_kb.add(button_settings_bestchange_garantex)
    inline_settings_kb.add(inline_btn_back)
    if len(inline_settings_kb.inline_keyboard) == 1:
        await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                    text="У Вас нет активных подписок, перейдите в главное меню и оплатите подписку",
                                    reply_markup=inline_back_main_kb)
        await bot.answer_callback_query(callback_query.id)
    else:
        await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                    text="Выберите схему для настройки", reply_markup=inline_settings_kb)
        await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == 'button_settings_bin_gar' or c.data == 'button_back_bingar')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text="Настройка Binance-Garantex-Bitzlato",
                                reply_markup=inline_binance_garantex_settings_kb)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == 'button_settings_bch_gin')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text="Настройка BestChange-Binance",
                                reply_markup=inline_button_beschange_binance_kb)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == 'button_trade_settings')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text="Торговля", reply_markup=inline_trade_settings_kb)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == 'button_upper_limit')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Какой у Вас верхний лимит на покупку/продажу в рублях?\n\nНапишите число без точек, "
                                "запятых и других символов")
    await bot.answer_callback_query(callback_query.id)
    await Cases.STATE_VOLUME.set()


@dp.message_handler(state=Cases.STATE_VOLUME)
async def settings(message: types.Message, state: FSMContext):
    volume_text = message.text
    if volume_text.isdigit():
        sql_command("""UPDATE settings_binance_garantex SET volume = ? WHERE userid = ?;""",
                    params=(volume_text, message.chat.id), data_base_name='settings_binance_garantex.db')
        await message.reply("Теперь ваш верхний лимит: {:,} ₽".format(int(volume_text)).replace(',', ' '), reply=False,
                            reply_markup=inline_trade_settings_kb)
        await state.reset_state()
    else:
        await message.reply("Ошибка ввода, попробуйте еще раз")


@dp.callback_query_handler(lambda c: c.data == 'button_down_limit')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Какой у Вас нижний лимит на покупку/продажу в рублях?\n\nНапишите число без точек, "
                                "запятых и других символов")
    await bot.answer_callback_query(callback_query.id)
    await Cases.STATE_MIN_LIM.set()


@dp.message_handler(state=Cases.STATE_MIN_LIM)
async def settings(message: types.Message, state: FSMContext):
    volume_text = message.text
    if volume_text.isdigit():
        sql_command("""UPDATE settings_binance_garantex SET min_amount = ? WHERE userid = ?;""",
                    params=(volume_text, message.chat.id), data_base_name='settings_binance_garantex.db')
        await message.reply("Теперь ваш нижний лимит: {:,} ₽".format(int(volume_text)).replace(',', ' '), reply=False,
                            reply_markup=inline_trade_settings_kb)
        await state.reset_state()
    else:
        await message.reply("Ошибка ввода, попробуйте еще раз")


@dp.callback_query_handler(lambda c: c.data == 'button_bingar_percent')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="При каком проценте присылать уведомления о спреде?\n\nНапишите число через точку "
                                "без других знкаов (Пример: 0.7)")
    await bot.answer_callback_query(callback_query.id)
    await Cases.STATE_PERCENT_BIN_GAR.set()


@dp.callback_query_handler(lambda c: c.data == 'button_bchbin_percent')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="При каком проценте присылать уведомления о спреде?\n\nНапишите число через точку "
                                "без других знкаов (Пример: 0.7)")
    await bot.answer_callback_query(callback_query.id)
    await Cases.STATE_PERCENT_BCH_BIN.set()


@dp.message_handler(state=Cases.STATE_PERCENT_BCH_BIN)
async def settings(message: types.Message, state: FSMContext):
    percent_text = message.text
    if percent_text.replace('.', '', 1).replace('-', '', 1).isdigit():
        sql_command("""UPDATE settings_bestchange_binance SET percent = ? WHERE userid = ?;""",
                    params=(percent_text, message.chat.id), data_base_name='settings_bestchange_binance.db')
        await message.reply("Ваш процент: {} %".format(percent_text), reply_markup=inline_main_kb,
                            reply=False)
        await state.reset_state()
    else:
        await message.reply('Ошибка ввода, попробуйте еще раз')


@dp.message_handler(state=Cases.STATE_PERCENT_BIN_GAR)
async def settings(message: types.Message, state: FSMContext):
    percent_text = message.text
    if percent_text.replace('.', '', 1).replace('-', '', 1).isdigit():
        sql_command("""UPDATE settings_binance_garantex SET percent = ? WHERE userid = ?;""",
                    params=(percent_text, message.chat.id), data_base_name='settings_binance_garantex.db')
        await message.reply("Ваш процент: {} %".format(percent_text), reply_markup=inline_trade_settings_kb,
                            reply=False)
        await state.reset_state()
    else:
        await message.reply('Ошибка ввода, попробуйте еще раз')


@dp.callback_query_handler(
    lambda c: c.data == 'button_bingar_paymeth'
              or c.data == 'button_tink_bin_gar_yes'
              or c.data == 'button_tink_bin_gar_no'
              or c.data == 'button_sber_bin_gar_yes'
              or c.data == 'button_sber_bin_gar_no')
async def process_callback_button1(callback_query: types.CallbackQuery):
    message_user_id = callback_query.from_user.id

    inline_trade_paymeth_bingar_kb = InlineKeyboardMarkup()

    if callback_query.data == 'button_tink_bin_gar_yes':
        sql_command("""UPDATE settings_binance_garantex SET payment_method_tinkoff = ? WHERE userid = ?;""",
                    params=(0, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_tink_bin_gar_no':
        sql_command("""UPDATE settings_binance_garantex SET payment_method_tinkoff = ? WHERE userid = ?;""",
                    params=(1, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_sber_bin_gar_yes':
        sql_command("""UPDATE settings_binance_garantex SET payment_method_sberbank = ? WHERE userid = ?;""",
                    params=(0, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_sber_bin_gar_no':
        sql_command("""UPDATE settings_binance_garantex SET payment_method_sberbank = ? WHERE userid = ?;""",
                    params=(1, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')

    p_method_tink = sql_command(
        "SELECT payment_method_tinkoff FROM settings_binance_garantex WHERE userid = ?;", params=(message_user_id,),
        data_base_name='settings_binance_garantex.db')

    p_method_sber = sql_command(
        "SELECT payment_method_sberbank FROM settings_binance_garantex WHERE userid = ?;", params=(message_user_id,),
        data_base_name='settings_binance_garantex.db')

    if p_method_tink[0][0]:
        inline_trade_paymeth_bingar_kb.add(inline_button_bingar_tink_yes)
    else:
        inline_trade_paymeth_bingar_kb.add(inline_button_bingar_tink_no)
    if p_method_sber[0][0]:
        inline_trade_paymeth_bingar_kb.add(inline_button_bingar_sber_yes)
    else:
        inline_trade_paymeth_bingar_kb.add(inline_button_bingar_sber_no)

    inline_trade_paymeth_bingar_kb.add(inline_button_back_bingar)

    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text="Включенные методы оплаты помечены ✔. Выключенные ❌. Нажмите чтобы изменить",
                                reply_markup=inline_trade_paymeth_bingar_kb)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(
    lambda c: c.data == 'button_binance_settings'
              or c.data == 'button_bingar_bin_eth_no'
              or c.data == 'button_bingar_bin_eth_yes'
              or c.data == 'button_bingar_bin_usdt_no'
              or c.data == 'button_bingar_bin_usdt_yes'
              or c.data == 'button_bingar_bin_btc_no'
              or c.data == 'button_bingar_bin_btc_yes')
async def process_callback_button1(callback_query: types.CallbackQuery):
    message_user_id = callback_query.from_user.id

    inline_exchange_bingar_kb = InlineKeyboardMarkup()

    if callback_query.data == 'button_bingar_bin_eth_no':
        sql_command("""UPDATE settings_binance_garantex SET is_binance_eth = ? WHERE userid = ?;""",
                    params=(1, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_bingar_bin_eth_yes':
        sql_command("""UPDATE settings_binance_garantex SET is_binance_eth = ? WHERE userid = ?;""",
                    params=(0, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_bingar_bin_usdt_no':
        sql_command("""UPDATE settings_binance_garantex SET is_binance_usdt = ? WHERE userid = ?;""",
                    params=(1, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_bingar_bin_usdt_yes':
        sql_command("""UPDATE settings_binance_garantex SET is_binance_usdt = ? WHERE userid = ?;""",
                    params=(0, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_bingar_bin_btc_no':
        sql_command("""UPDATE settings_binance_garantex SET is_binance_btc = ? WHERE userid = ?;""",
                    params=(1, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_bingar_bin_btc_yes':
        sql_command("""UPDATE settings_binance_garantex SET is_binance_btc = ? WHERE userid = ?;""",
                    params=(0, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')

    is_eth_bin = sql_command(
        "SELECT is_binance_eth FROM settings_binance_garantex WHERE userid = ?;", params=(message_user_id,),
        data_base_name='settings_binance_garantex.db')

    is_usdt_bin = sql_command(
        "SELECT is_binance_usdt FROM settings_binance_garantex WHERE userid = ?;", params=(message_user_id,),
        data_base_name='settings_binance_garantex.db')

    is_btc_bin = sql_command(
        "SELECT is_binance_btc FROM settings_binance_garantex WHERE userid = ?;", params=(message_user_id,),
        data_base_name='settings_binance_garantex.db')

    if is_eth_bin[0][0]:
        inline_exchange_bingar_kb.add(inline_button_bingar_bin_eth_yes)
    else:
        inline_exchange_bingar_kb.add(inline_button_bingar_bin_eth_no)
    if is_usdt_bin[0][0]:
        inline_exchange_bingar_kb.add(inline_button_bingar_bin_usdt_yes)
    else:
        inline_exchange_bingar_kb.add(inline_button_bingar_bin_usdt_no)
    if is_btc_bin[0][0]:
        inline_exchange_bingar_kb.add(inline_button_bingar_bin_btc_yes)
    else:
        inline_exchange_bingar_kb.add(inline_button_bingar_bin_btc_no)

    inline_exchange_bingar_kb.add(inline_button_back_bingar)

    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text="Настроить Binance\n\nВключенные валюты помечены ✔. \n\nВыключенные ❌. \n\nНажмите чтобы изменить",
                                reply_markup=inline_exchange_bingar_kb)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(
    lambda c: c.data == 'button_garantex_settings'
              or c.data == 'button_bingar_gar_eth_no'
              or c.data == 'button_bingar_gar_eth_yes'
              or c.data == 'button_bingar_gar_usdt_no'
              or c.data == 'button_bingar_gar_usdt_yes'
              or c.data == 'button_bingar_gar_btc_no'
              or c.data == 'button_bingar_gar_btc_yes')
async def process_callback_button1(callback_query: types.CallbackQuery):
    message_user_id = callback_query.from_user.id

    inline_exchange_bingar_kb = InlineKeyboardMarkup()

    if callback_query.data == 'button_bingar_gar_eth_no':
        sql_command("""UPDATE settings_binance_garantex SET is_garantex_eth = ? WHERE userid = ?;""",
                    params=(1, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_bingar_gar_eth_yes':
        sql_command("""UPDATE settings_binance_garantex SET is_garantex_eth = ? WHERE userid = ?;""",
                    params=(0, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_bingar_gar_usdt_no':
        sql_command("""UPDATE settings_binance_garantex SET is_garantex_usdt = ? WHERE userid = ?;""",
                    params=(1, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_bingar_gar_usdt_yes':
        sql_command("""UPDATE settings_binance_garantex SET is_garantex_usdt = ? WHERE userid = ?;""",
                    params=(0, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_bingar_gar_btc_no':
        sql_command("""UPDATE settings_binance_garantex SET is_garantex_btc = ? WHERE userid = ?;""",
                    params=(1, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_bingar_gar_btc_yes':
        sql_command("""UPDATE settings_binance_garantex SET is_garantex_btc = ? WHERE userid = ?;""",
                    params=(0, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')

    is_eth_gar = sql_command(
        "SELECT is_garantex_eth FROM settings_binance_garantex WHERE userid = ?;", params=(message_user_id,),
        data_base_name='settings_binance_garantex.db')

    is_usdt_gar = sql_command(
        "SELECT is_garantex_usdt FROM settings_binance_garantex WHERE userid = ?;", params=(message_user_id,),
        data_base_name='settings_binance_garantex.db')

    is_btc_gar = sql_command(
        "SELECT is_garantex_btc FROM settings_binance_garantex WHERE userid = ?;", params=(message_user_id,),
        data_base_name='settings_binance_garantex.db')

    if is_eth_gar[0][0]:
        inline_exchange_bingar_kb.add(inline_button_bingar_gar_eth_yes)
    else:
        inline_exchange_bingar_kb.add(inline_button_bingar_gar_eth_no)
    if is_usdt_gar[0][0]:
        inline_exchange_bingar_kb.add(inline_button_bingar_gar_usdt_yes)
    else:
        inline_exchange_bingar_kb.add(inline_button_bingar_gar_usdt_no)
    if is_btc_gar[0][0]:
        inline_exchange_bingar_kb.add(inline_button_bingar_gar_btc_yes)
    else:
        inline_exchange_bingar_kb.add(inline_button_bingar_gar_btc_no)

    inline_exchange_bingar_kb.add(inline_button_back_bingar)

    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text="Настроить Garantex\n\nВключенные валюты помечены ✔. \n\nВыключенные ❌. \n\nНажмите чтобы изменить",
                                reply_markup=inline_exchange_bingar_kb)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(
    lambda c: c.data == 'button_bitzlato_settings'
              or c.data == 'button_bingar_bz_eth_no'
              or c.data == 'button_bingar_bz_eth_yes'
              or c.data == 'button_bingar_bz_usdt_no'
              or c.data == 'button_bingar_bz_usdt_yes'
              or c.data == 'button_bingar_bz_btc_no'
              or c.data == 'button_bingar_bz_btc_yes')
async def process_callback_button1(callback_query: types.CallbackQuery):
    message_user_id = callback_query.from_user.id

    inline_exchange_bingar_kb = InlineKeyboardMarkup()

    if callback_query.data == 'button_bingar_bz_eth_no':
        sql_command("""UPDATE settings_binance_garantex SET is_bz_eth = ? WHERE userid = ?;""",
                    params=(1, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_bingar_bz_eth_yes':
        sql_command("""UPDATE settings_binance_garantex SET is_bz_eth = ? WHERE userid = ?;""",
                    params=(0, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_bingar_bz_usdt_no':
        sql_command("""UPDATE settings_binance_garantex SET is_bz_usdt = ? WHERE userid = ?;""",
                    params=(1, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_bingar_bz_usdt_yes':
        sql_command("""UPDATE settings_binance_garantex SET is_bz_usdt = ? WHERE userid = ?;""",
                    params=(0, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_bingar_bz_btc_no':
        sql_command("""UPDATE settings_binance_garantex SET is_bz_btc = ? WHERE userid = ?;""",
                    params=(1, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')
    if callback_query.data == 'button_bingar_bz_btc_yes':
        sql_command("""UPDATE settings_binance_garantex SET is_bz_btc = ? WHERE userid = ?;""",
                    params=(0, callback_query.from_user.id), data_base_name='settings_binance_garantex.db')

    is_eth_bz = sql_command(
        "SELECT is_bz_eth FROM settings_binance_garantex WHERE userid = ?;", params=(message_user_id,),
        data_base_name='settings_binance_garantex.db')

    is_usdt_bz = sql_command(
        "SELECT is_bz_usdt FROM settings_binance_garantex WHERE userid = ?;", params=(message_user_id,),
        data_base_name='settings_binance_garantex.db')

    is_btc_bz = sql_command(
        "SELECT is_bz_btc FROM settings_binance_garantex WHERE userid = ?;", params=(message_user_id,),
        data_base_name='settings_binance_garantex.db')

    if is_eth_bz[0][0]:
        inline_exchange_bingar_kb.add(inline_button_bingar_bz_eth_yes)
    else:
        inline_exchange_bingar_kb.add(inline_button_bingar_bz_eth_no)
    if is_usdt_bz[0][0]:
        inline_exchange_bingar_kb.add(inline_button_bingar_bz_usdt_yes)
    else:
        inline_exchange_bingar_kb.add(inline_button_bingar_bz_usdt_no)
    if is_btc_bz[0][0]:
        inline_exchange_bingar_kb.add(inline_button_bingar_bz_btc_yes)
    else:
        inline_exchange_bingar_kb.add(inline_button_bingar_bz_btc_no)

    inline_exchange_bingar_kb.add(inline_button_back_bingar)

    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text="Настроить Bitzlato\n\nВключенные валюты помечены ✔. "
                                     "\n\nВыключенные ❌. \n\nНажмите чтобы изменить",
                                reply_markup=inline_exchange_bingar_kb)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == 'button_exchanges_settings')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text="Настройка бирж", reply_markup=inline_button_exchange_kb)
    await bot.answer_callback_query(callback_query.id)


if __name__ == '__main__':
    executor.start_polling(dp)
