from aiogram.dispatcher.filters.state import StatesGroup, State


class Cases(StatesGroup):
    STATE_SETTINGS = State()
    STATE_PAYMENT = State()
    STATE_VOLUME = State()
    STATE_METHOD = State()
    STATE_NICK = State()
    STATE_PERCENT = State()
    STATE_MIN_AMOUNT = State()
    STATE_CHANGE_BINANCE_COIN_SETTINGS = State()
    STATE_CHANGE_GARANTEX_COIN_SETTINGS = State()
    STATE_CHANGE_BITZLATO_COIN_SETTINGS = State()
    SUB_STATE_SETTINGS = State()
    STATE_EXCH_SETTINGS = State()
    STATE_TRADE_SETTINGS = State()
