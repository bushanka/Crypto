from aiogram.dispatcher.filters.state import StatesGroup, State


class Cases(StatesGroup):
    STATE_CHANGE_TIME_BIN_GAR_BZ = State()
    STATE_UNSUBSCRIBE_BIN_GAR_BZ = State()
    STATE_SUBSCRIBE_BIN_GAR_BZ = State()
    STATE_CHANGE_TIME_BCH_BIN = State()
    STATE_UNSUBSCRIBE_BCH_BIN = State()
    STATE_SUBSCRIBE_BCH_BIN = State()
