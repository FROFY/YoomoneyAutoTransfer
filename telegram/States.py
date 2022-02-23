from aiogram.dispatcher.filters.state import StatesGroup, State


class StatesBot(StatesGroup):
    token_add = State()
    token_delete = State()
    balance_checking = State()
