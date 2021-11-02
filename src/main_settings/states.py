from aiogram.dispatcher.filters.state import StatesGroup, State


class Cases(StatesGroup):
    STATE_VOLUME = State()
    STATE_MIN_LIM = State()
    STATE_PERCENT_BIN_GAR = State()
    STATE_PERCENT_BCH_BIN = State()
