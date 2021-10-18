from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from states import Cases
from datetime import date

# Bot create
bot = Bot(token='1971360278:AAEmqzP0fKTi2a_eaNcMMLn0386ouLuwIT0')
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# KeyBoard and buttons
button_settings = KeyboardButton('Настройки ⚙')
button_help = KeyboardButton('Помощь 🚑')
button_subscribe = KeyboardButton('Оплата подписки 💵')
button_pay = KeyboardButton('Не сегодня!')
button_volume = KeyboardButton('Объемы')
button_pay_meth = KeyboardButton('Методы оплаты')
button_nick_binance = KeyboardButton('Мой ник на Binance')
button_settings_exit = KeyboardButton('Назад')
button_pay_tinkoff = KeyboardButton('Тинькофф')
button_pay_sber = KeyboardButton('Сбербанк')
button_pay_tinkoff_and_sber = KeyboardButton('Тинькофф или Сбербанк')
button_percent = KeyboardButton('Процент')
button_min_amount = KeyboardButton('Нижний лимит')
button_binance_settings = KeyboardButton('Настроить Binance')
button_garantex_settings = KeyboardButton('Настроить Garantex')
button_bitzlato_settings = KeyboardButton('Настроить Bitzlato')
button_exchanges = KeyboardButton('Биржи')
button_money_settings = KeyboardButton('Торговля')

main_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_kb.add(button_settings, button_subscribe)
# main_kb.add(button_subscribe)
# main_kb.add(button_help)

pay_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
pay_kb.add(button_pay)

settings_kb_exch = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
settings_kb_exch.add(button_binance_settings, button_garantex_settings, button_bitzlato_settings, button_settings_exit)

settings_kb_trade = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
settings_kb_trade.add(button_volume, button_pay_meth, button_percent, button_min_amount, button_settings_exit)

pay_methods_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
pay_methods_kb.add(button_pay_tinkoff, button_pay_sber, button_pay_tinkoff_and_sber)

sub_settings_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
sub_settings_kb.add(button_exchanges, button_money_settings, button_settings_exit)


def sql_command(command_text, params=None):
    connection = False
    data = None
    try:
        connection = sqlite3.connect('data.db')
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


sql_command("""CREATE TABLE IF NOT EXISTS users_data(
"userid" INT PRIMARY KEY,
"username" TEXT,
"subscriber" INTEGER DEFAULT 0,
"volume" TEXT DEFAULT 100000,
"payment_methods" TEXT DEFAULT 'Tinkoff',
"test_access" TEXT DEFAULT 'Yes',
"time_subscribe" TEXT,
"percent" REAL DEFAULT 0,
"min_amount" INTEGER DEFAULT 5000,
"is_binance_usdt" INTEGER DEFAULT 1,
"is_binance_eth" INTEGER DEFAULT 1,
"is_binance_btc" INTEGER DEFAULT 1);""")


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    message_user = [message.chat.id, message.chat.username]
    data = sql_command("SELECT userid FROM users_data WHERE userid = ?;", params=(message_user[0],))
    if data is None:
        sql_command("""INSERT INTO users_data(userid, username) VALUES(?,?);""", message_user)
        today = date.today()
        d = today.strftime('%Y-%m-%d')
        sql_command("""UPDATE users_data SET subscriber = ? WHERE userid = ?;""", (1, message_user[0]))
        sql_command("""UPDATE users_data SET time_subscribe = ? WHERE userid = ?;""", (d, message_user[0]))
        sql_command("""UPDATE users_data SET test_access = ? WHERE userid = ?;""", ('Yes', message_user[0]))
        sql_command("""UPDATE users_data SET percent = ? WHERE userid = ?;""", (0.1, message_user[0]))
    await message.reply(
        "Привет!\n\nТут можно настроить бота\n\n"
        "Чтобы рассылка заработала нужно запустить этого бота: @BestLoopsBot\nПросто напиши ему /start",
        reply_markup=main_kb, reply=False)


@dp.message_handler(lambda message: message.text == 'Помощь 🚑')
async def process_help_command(message: types.Message):
    await message.reply("По всем вопросам\nпишите сюда 👉 @Captain_Danny", reply_markup=main_kb, reply=False)


@dp.message_handler(lambda message: message.text == 'Оплата подписки 💵')
async def process_subscribe_command(message: types.Message):
    subscr_id = str(message.chat.id)
    await message.reply("Чтобы продлить подписку на месяц, переведите 29 USDT на один из адресов:",
                        reply_markup=main_kb, reply=False)
    await message.reply(
        "BSC(BEP20): 0x93f5e1069a1cd94c4166c5060b770563fbba12de\n\nTron(TRC20): TE8FdD1RWiBvMsEMdtk5FJwvDQBF2vt7Ai",
        reply=False)
    await message.reply(
        "Используйте биржу Binance\n\nПосле оплаты напишите @e_usovchan что Вы оплатили\nи в сообщении укажите Ваш ID:",
        reply=False)
    await message.reply(subscr_id, reply=False, reply_markup=main_kb)


@dp.message_handler(lambda message: message.text == 'Настройки ⚙')
async def process_settings_command(message: types.Message):
    await message.reply("Здесь можно настроить бота", reply_markup=sub_settings_kb, reply=False)
    await Cases.SUB_STATE_SETTINGS.set()


@dp.message_handler(lambda message: message.text == 'Биржи', state=Cases.SUB_STATE_SETTINGS)
async def process_settings_command(message: types.Message):
    await message.reply("Настройка биржи", reply_markup=settings_kb_exch, reply=False)
    await Cases.STATE_EXCH_SETTINGS.set()


@dp.message_handler(lambda message: message.text == 'Торговля', state=Cases.SUB_STATE_SETTINGS)
async def process_settings_command(message: types.Message):
    await message.reply("Настройка торговли", reply_markup=settings_kb_trade, reply=False)
    await Cases.STATE_TRADE_SETTINGS.set()


@dp.message_handler(lambda message: message.text == 'Назад', state=Cases.STATE_EXCH_SETTINGS)
async def process_settings_command(message: types.Message):
    await message.reply("Готово", reply_markup=sub_settings_kb, reply=False)
    await Cases.SUB_STATE_SETTINGS.set()


@dp.message_handler(lambda message: message.text == 'Назад', state=Cases.STATE_TRADE_SETTINGS)
async def process_settings_command(message: types.Message):
    await message.reply("Готово", reply_markup=sub_settings_kb, reply=False)
    await Cases.SUB_STATE_SETTINGS.set()


@dp.message_handler(lambda message: message.text == 'Объемы', state=Cases.STATE_TRADE_SETTINGS)
async def settings(message: types.Message):
    await message.reply(
        "Какие у Вас объемы на покупку/продажу в рублях?\n\nНапишите число без точек, запятых и других символов",
        reply_markup=main_kb, reply=False)
    await Cases.STATE_VOLUME.set()


def exchange_settings_buttons(exch, mes):
    data = sql_command("""SELECT * from users_data WHERE userid = ?""", (mes.chat.id,))
    rec_list = data[0]
    bin_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if exch == 'Binance':
        if rec_list[10] == 1 and rec_list[11] == 1 and rec_list[12] == 1:
            bin_kb.add(KeyboardButton('Выключить USDT'), KeyboardButton('Выключить ETH'),
                       KeyboardButton('Выключить BTC'))
        elif rec_list[10] == 1 and rec_list[11] == 1 and rec_list[12] == 0:
            bin_kb.add(KeyboardButton('Выключить USDT'), KeyboardButton('Выключить ETH'),
                       KeyboardButton('Включить BTC'))
        elif rec_list[10] == 1 and rec_list[11] == 0 and rec_list[12] == 1:
            bin_kb.add(KeyboardButton('Выключить USDT'), KeyboardButton('Включить ETH'),
                       KeyboardButton('Выключить BTC'))
        elif rec_list[10] == 1 and rec_list[11] == 0 and rec_list[12] == 0:
            bin_kb.add(KeyboardButton('Выключить USDT'), KeyboardButton('Включить ETH'), KeyboardButton('Включить BTC'))
        elif rec_list[10] == 0 and rec_list[11] == 1 and rec_list[12] == 1:
            bin_kb.add(KeyboardButton('Включить USDT'), KeyboardButton('Выключить ETH'),
                       KeyboardButton('Выключить BTC'))
        elif rec_list[10] == 0 and rec_list[11] == 1 and rec_list[12] == 0:
            bin_kb.add(KeyboardButton('Включить USDT'), KeyboardButton('Выключить ETH'), KeyboardButton('Включить BTC'))
        elif rec_list[10] == 0 and rec_list[11] == 0 and rec_list[12] == 1:
            bin_kb.add(KeyboardButton('Включить USDT'), KeyboardButton('Включить ETH'), KeyboardButton('Выключить BTC'))
        elif rec_list[10] == 0 and rec_list[11] == 0 and rec_list[12] == 0:
            bin_kb.add(KeyboardButton('Включить USDT'), KeyboardButton('Включить ETH'), KeyboardButton('Включить BTC'))
    if exch == 'Garantex':
        if rec_list[13] == 1 and rec_list[14] == 1 and rec_list[15] == 1:
            bin_kb.add(KeyboardButton('Выключить USDT'), KeyboardButton('Выключить ETH'),
                       KeyboardButton('Выключить BTC'))
        elif rec_list[13] == 1 and rec_list[14] == 1 and rec_list[15] == 0:
            bin_kb.add(KeyboardButton('Выключить USDT'), KeyboardButton('Выключить ETH'),
                       KeyboardButton('Включить BTC'))
        elif rec_list[13] == 1 and rec_list[14] == 0 and rec_list[15] == 1:
            bin_kb.add(KeyboardButton('Выключить USDT'), KeyboardButton('Включить ETH'),
                       KeyboardButton('Выключить BTC'))
        elif rec_list[13] == 1 and rec_list[14] == 0 and rec_list[15] == 0:
            bin_kb.add(KeyboardButton('Выключить USDT'), KeyboardButton('Включить ETH'), KeyboardButton('Включить BTC'))
        elif rec_list[13] == 0 and rec_list[14] == 1 and rec_list[15] == 1:
            bin_kb.add(KeyboardButton('Включить USDT'), KeyboardButton('Выключить ETH'),
                       KeyboardButton('Выключить BTC'))
        elif rec_list[13] == 0 and rec_list[14] == 1 and rec_list[15] == 0:
            bin_kb.add(KeyboardButton('Включить USDT'), KeyboardButton('Выключить ETH'), KeyboardButton('Включить BTC'))
        elif rec_list[13] == 0 and rec_list[14] == 0 and rec_list[15] == 1:
            bin_kb.add(KeyboardButton('Включить USDT'), KeyboardButton('Включить ETH'), KeyboardButton('Выключить BTC'))
        elif rec_list[13] == 0 and rec_list[14] == 0 and rec_list[15] == 0:
            bin_kb.add(KeyboardButton('Включить USDT'), KeyboardButton('Включить ETH'), KeyboardButton('Включить BTC'))
    if exch == 'Bitzlato':
        if rec_list[16] == 1 and rec_list[17] == 1 and rec_list[18] == 1:
            bin_kb.add(KeyboardButton('Выключить USDT'), KeyboardButton('Выключить ETH'),
                       KeyboardButton('Выключить BTC'))
        elif rec_list[16] == 1 and rec_list[17] == 1 and rec_list[18] == 0:
            bin_kb.add(KeyboardButton('Выключить USDT'), KeyboardButton('Выключить ETH'),
                       KeyboardButton('Включить BTC'))
        elif rec_list[16] == 1 and rec_list[17] == 0 and rec_list[18] == 1:
            bin_kb.add(KeyboardButton('Выключить USDT'), KeyboardButton('Включить ETH'),
                       KeyboardButton('Выключить BTC'))
        elif rec_list[16] == 1 and rec_list[17] == 0 and rec_list[18] == 0:
            bin_kb.add(KeyboardButton('Выключить USDT'), KeyboardButton('Включить ETH'), KeyboardButton('Включить BTC'))
        elif rec_list[16] == 0 and rec_list[17] == 1 and rec_list[18] == 1:
            bin_kb.add(KeyboardButton('Включить USDT'), KeyboardButton('Выключить ETH'),
                       KeyboardButton('Выключить BTC'))
        elif rec_list[16] == 0 and rec_list[17] == 1 and rec_list[18] == 0:
            bin_kb.add(KeyboardButton('Включить USDT'), KeyboardButton('Выключить ETH'), KeyboardButton('Включить BTC'))
        elif rec_list[16] == 0 and rec_list[17] == 0 and rec_list[18] == 1:
            bin_kb.add(KeyboardButton('Включить USDT'), KeyboardButton('Включить ETH'), KeyboardButton('Выключить BTC'))
        elif rec_list[16] == 0 and rec_list[17] == 0 and rec_list[18] == 0:
            bin_kb.add(KeyboardButton('Включить USDT'), KeyboardButton('Включить ETH'), KeyboardButton('Включить BTC'))
    bin_kb.add(KeyboardButton('Назад'))
    return bin_kb


@dp.message_handler(lambda message: message.text == 'Настроить Binance', state=Cases.STATE_EXCH_SETTINGS)
async def settings(message: types.Message):
    bin_kb = exchange_settings_buttons('Binance', mes=message)
    await message.reply("Выберите какие монеты включить/выключить для отображения", reply_markup=bin_kb, reply=False)
    await Cases.STATE_CHANGE_BINANCE_COIN_SETTINGS.set()


@dp.message_handler(lambda message: message.text == 'Настроить Garantex', state=Cases.STATE_EXCH_SETTINGS)
async def settings(message: types.Message):
    bin_kb = exchange_settings_buttons('Garantex', mes=message)
    await message.reply("Выберите какие монеты включить/выключить для отображения", reply_markup=bin_kb, reply=False)
    await Cases.STATE_CHANGE_GARANTEX_COIN_SETTINGS.set()


@dp.message_handler(lambda message: message.text == 'Настроить Bitzlato', state=Cases.STATE_EXCH_SETTINGS)
async def settings(message: types.Message):
    bin_kb = exchange_settings_buttons('Bitzlato', mes=message)
    await message.reply(
        "Выберите какие монеты включить/выключить для отображения",
        reply_markup=bin_kb, reply=False)
    await Cases.STATE_CHANGE_BITZLATO_COIN_SETTINGS.set()


@dp.message_handler(lambda message: message.text == 'Методы оплаты', state=Cases.STATE_TRADE_SETTINGS)
async def settings(message: types.Message):
    await message.reply(
        "Выберите метод оплаты, используя клавиатуру",
        reply_markup=pay_methods_kb, reply=False)
    await Cases.STATE_METHOD.set()


@dp.message_handler(state=Cases.STATE_CHANGE_BINANCE_COIN_SETTINGS)
async def settings(message: types.Message):
    if message.text == 'Выключить USDT':
        sql_command("""UPDATE users_data SET is_binance_usdt = ? WHERE userid = ?;""", (0, message.chat.id))
        bin_kb = exchange_settings_buttons('Binance', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Выключить ETH':
        sql_command("""UPDATE users_data SET is_binance_eth = ? WHERE userid = ?;""", (0, message.chat.id))
        bin_kb = exchange_settings_buttons('Binance', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Выключить BTC':
        sql_command("""UPDATE users_data SET is_binance_btc = ? WHERE userid = ?;""", (0, message.chat.id))
        bin_kb = exchange_settings_buttons('Binance', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Включить USDT':
        sql_command("""UPDATE users_data SET is_binance_usdt = ? WHERE userid = ?;""", (1, message.chat.id))
        bin_kb = exchange_settings_buttons('Binance', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Включить ETH':
        sql_command("""UPDATE users_data SET is_binance_eth = ? WHERE userid = ?;""", (1, message.chat.id))
        bin_kb = exchange_settings_buttons('Binance', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Включить BTC':
        sql_command("""UPDATE users_data SET is_binance_btc = ? WHERE userid = ?;""", (1, message.chat.id))
        bin_kb = exchange_settings_buttons('Binance', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Назад':
        await message.reply('Готово', reply=False, reply_markup=settings_kb_exch)
        await Cases.STATE_EXCH_SETTINGS.set()
    else:
        await message.reply("Используйте кнопки, поробуйте еще раз", reply=False, reply_markup=settings_kb_exch)


@dp.message_handler(state=Cases.STATE_CHANGE_GARANTEX_COIN_SETTINGS)
async def settings(message: types.Message):
    if message.text == 'Выключить USDT':
        sql_command("""UPDATE users_data SET is_garantex_usdt = ? WHERE userid = ?;""", (0, message.chat.id))

        bin_kb = exchange_settings_buttons('Garantex', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Выключить ETH':
        sql_command("""UPDATE users_data SET is_garantex_eth = ? WHERE userid = ?;""", (0, message.chat.id))
        bin_kb = exchange_settings_buttons('Garantex', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Выключить BTC':
        sql_command("""UPDATE users_data SET is_garantex_btc = ? WHERE userid = ?;""", (0, message.chat.id))

        bin_kb = exchange_settings_buttons('Garantex', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Включить USDT':
        sql_command("""UPDATE users_data SET is_garantex_usdt = ? WHERE userid = ?;""", (1, message.chat.id))

        bin_kb = exchange_settings_buttons('Garantex', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Включить ETH':
        sql_command("""UPDATE users_data SET is_garantex_eth = ? WHERE userid = ?;""", (1, message.chat.id))

        bin_kb = exchange_settings_buttons('Garantex', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Включить BTC':
        sql_command("""UPDATE users_data SET is_garantex_btc = ? WHERE userid = ?;""", (1, message.chat.id))

        bin_kb = exchange_settings_buttons('Garantex', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Назад':
        await message.reply('Готово', reply=False, reply_markup=settings_kb_exch)
        await Cases.STATE_EXCH_SETTINGS.set()
    else:
        await message.reply("Используйте кнопки, поробуйте еще раз", reply=False, reply_markup=settings_kb_exch)


@dp.message_handler(state=Cases.STATE_CHANGE_BITZLATO_COIN_SETTINGS)
async def settings(message: types.Message):
    if message.text == 'Выключить USDT':
        sql_command("""UPDATE users_data SET is_bz_usdt = ? WHERE userid = ?;""", (0, message.chat.id))

        bin_kb = exchange_settings_buttons('Bitzlato', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Выключить ETH':
        sql_command("""UPDATE users_data SET is_bz_eth = ? WHERE userid = ?;""", (0, message.chat.id))

        bin_kb = exchange_settings_buttons('Bitzlato', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Выключить BTC':
        sql_command("""UPDATE users_data SET is_bz_btc = ? WHERE userid = ?;""", (0, message.chat.id))

        bin_kb = exchange_settings_buttons('Bitzlato', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Включить USDT':
        sql_command("""UPDATE users_data SET is_bz_usdt = ? WHERE userid = ?;""", (1, message.chat.id))

        bin_kb = exchange_settings_buttons('Bitzlato', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Включить ETH':
        sql_command("""UPDATE users_data SET is_bz_eth = ? WHERE userid = ?;""", (1, message.chat.id))

        bin_kb = exchange_settings_buttons('Bitzlato', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Включить BTC':
        sql_command("""UPDATE users_data SET is_bz_btc = ? WHERE userid = ?;""", (1, message.chat.id))

        bin_kb = exchange_settings_buttons('Bitzlato', mes=message)
        await message.reply("Изменено", reply=False, reply_markup=bin_kb)
    elif message.text == 'Назад':
        await message.reply('Готово', reply=False, reply_markup=settings_kb_exch)
        await Cases.STATE_EXCH_SETTINGS.set()
    else:
        await message.reply("Используйте кнопки, поробуйте еще раз", reply=False, reply_markup=settings_kb_exch)


@dp.message_handler(lambda message: message.text == 'Назад', state=Cases.SUB_STATE_SETTINGS)
async def settings(message: types.Message, state: FSMContext):
    await message.reply(text='Настройка завершена', reply_markup=main_kb, reply=False)
    await state.reset_state()


@dp.message_handler(state=Cases.STATE_VOLUME)
async def settings(message: types.Message):
    volume_text = message.text
    if volume_text.isdigit():
        sql_command("""UPDATE users_data SET volume = ? WHERE userid = ?;""", (volume_text, message.chat.id))

        await message.reply("Теперь ваш объем: {:,} ₽".format(int(volume_text)), reply_markup=settings_kb_trade,
                            reply=False)
        await Cases.STATE_TRADE_SETTINGS.set()
    else:
        await message.reply("Ошибка ввода, попробуйте еще раз", reply_markup=sub_settings_kb, reply=False)


@dp.message_handler(state=Cases.STATE_METHOD)
async def settings(message: types.Message):
    method_text = message.text
    if method_text == 'Тинькофф':
        sql_command("""UPDATE users_data SET payment_methods = ? WHERE userid = ?;""", ('Tinkoff', message.chat.id))

        await message.reply(f"Ваши методы оплаты: {method_text}", reply_markup=settings_kb_trade, reply=False)
        await Cases.STATE_TRADE_SETTINGS.set()
    elif method_text == 'Сбербанк':
        sql_command("""UPDATE users_data SET payment_methods = ? WHERE userid = ?;""", ('Sberbank', message.chat.id))

        await message.reply(f"Ваши методы оплаты: {method_text}", reply_markup=settings_kb_trade, reply=False)
        await Cases.STATE_TRADE_SETTINGS.set()
    elif method_text == 'Тинькофф или Сбербанк':
        sql_command("""UPDATE users_data SET payment_methods = ? WHERE userid = ?;""",
                    ('Tinkoff,Sberbank', message.chat.id))

        await message.reply(f"Ваши методы оплаты: {method_text}", reply_markup=settings_kb_trade, reply=False)
        await Cases.STATE_TRADE_SETTINGS.set()
    else:
        await message.reply("Такие методы пока не поддерживаются, выберите, пожалуйста, другие",
                            reply_markup=pay_methods_kb, reply=False)


@dp.message_handler(lambda message: message.text == 'Процент', state=Cases.STATE_TRADE_SETTINGS)
async def settings(message: types.Message):
    await message.reply(
        "При каком проценте присылать уведомления о спреде?\n\nНапишите число через точку без других знкаов (Пример: 0.7)",
        reply_markup=main_kb, reply=False)
    await Cases.STATE_PERCENT.set()


@dp.message_handler(lambda message: message.text == 'Нижний лимит', state=Cases.STATE_TRADE_SETTINGS)
async def settings(message: types.Message):
    await message.reply(
        "На какую минимальную сумму хотите чтобы Вам продавали крипту? Напишите число без других символов",
        reply_markup=main_kb, reply=False)
    await Cases.STATE_MIN_AMOUNT.set()


@dp.message_handler(state=Cases.STATE_PERCENT)
async def settings(message: types.Message):
    percent_text = message.text
    if percent_text.replace('.', '', 1).replace('-', '', 1).isdigit():
        sql_command("""UPDATE users_data SET percent = ? WHERE userid = ?;""", (float(percent_text), message.chat.id))
        await message.reply("Ваш процент: {}".format(percent_text), reply_markup=settings_kb_trade, reply=False)
        await Cases.STATE_TRADE_SETTINGS.set()

    else:
        await message.reply('Ошибка ввода, попробуйте еще раз')


@dp.message_handler(state=Cases.STATE_MIN_AMOUNT)
async def settings(message: types.Message):
    percent_text = message.text
    if percent_text.isdigit():
        sql_command("""UPDATE users_data SET min_amount = ? WHERE userid = ?;""",
                    (float(percent_text), message.chat.id))

        await message.reply("Нижний лимит: {:,} ₽".format(int(percent_text)), reply_markup=settings_kb_trade,
                            reply=False)
        await Cases.STATE_TRADE_SETTINGS.set()

    else:
        await message.reply('Ошибка ввода, попробуйте еще раз')


if __name__ == '__main__':
    executor.start_polling(dp)
