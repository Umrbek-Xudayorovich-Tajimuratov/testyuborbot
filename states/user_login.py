from aiogram.fsm.state import StatesGroup, State

class UserData(StatesGroup):
    hemis_id = State()
    hemis_password = State()