from aiogram.fsm.state import StatesGroup, State


class ChangePassword(StatesGroup):
    chp = State()
